#!/usr/bin/env -S uv run --script

import json
import os
from typing import Tuple, List

import docker
import polars as pl

from aggregator.lab_data_read_and_normalise import retrieve
from common.folders import VEP_FOLDER, WORKING_FOLDER
from common.known_contigs import known_contig_to_chrom_map, known_37_contigs_list, known_38_contigs_list
from common.vcf_aggregate_counts_vep_parquet_types import (
    coord_columns,
    indexed_record_fields,
    vep_record_fields,
    lab_submitted_record_fields,
    lab_submitted_source_fields,
    labs_contributing_name,
    hom_count_name,
    het_count_name,
    source_name,
)

# the configuration of where we are going to get data from
sources = [
    ("sa", None, "../../PRIVATE/sa/"),
    ("vcgs", "vcgs-agha-variant-count-upload", "lab-counts/2025-01-22/"),
    ("pq", "s3-gen-pqmolgen-nagim-pqmolgen", "lab-counts/PQ_WES_to_NAGIM2.parquet"),
]


def aggregate(sources: List[Tuple[str,str,str]]):
    """
    Aggregate data from source labs.

    :param sources: a list of tuples of (short name, bucket, path)
    :return: a DataFrame of aggregated data
    """
    lab_combined = pl.DataFrame(
        schema=pl.Schema(lab_submitted_record_fields | lab_submitted_source_fields)
    )

    for lab_source in sources:
        print(lab_source[0].upper())
        print("---------------------")

        #lab_data, lab_msgs = retrieve(
        #   lab_source[0], lab_source[1], lab_source[2], False, None)

        # example limits for testing
        lab_data, lab_msgs = retrieve(
            lab_source[0], lab_source[1], lab_source[2], False, 5000)
        #lab_data, lab_msgs = retrieve(
        #    lab_source[0], lab_source[1], lab_source[2], False, "NC_000019.10")

        # output some useful warning messages related to each labs data
        for m in lab_msgs:
            print(f"  {m}")
        print("")

        lab_combined = lab_combined.vstack(lab_data)

    # aggregate the data from the various sources - keeping track of which source contributed to each count
    # we also add in a row index for future VEP processing
    agg_df = (
        lab_combined.group_by(coord_columns)
        .agg(
            pl.col(hom_count_name).sum(),
            pl.col(het_count_name).sum(),
            # our kwarg argument here is from a variable - hence our slightly wierd calling syntax
            **{labs_contributing_name: pl.col(source_name)},
        )
        .sort(by=coord_columns)
        .with_row_index()
    )

    return agg_df


def create_aggregate_vcf(df: pl.DataFrame, vcf_name: str, contig_to_include: List[str]):
    """
    Create a VCF file from records in our aggregate data frame. Has the minimal information possible
    for a VCF so we can pass it in bulk to VEP. Has no other grander purpose (as a VCF) than that.

    :param df: the DataFrame of variants
    :param vcf_name: the name of the VCF file to create in the working folder
    :param contig_to_include: a list of contigs to include (so we can filter for different reference genomes)
    :return:
    """
    with open(f"{WORKING_FOLDER}/{vcf_name}", "w") as input_vcf:
        # not needed for VEP but technically required for any VCF file
        input_vcf.write("##fileformat=VCFv4.2\n")
        input_vcf.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

        for row in df.iter_rows(named=True):
            if row["contig"] not in known_contig_to_chrom_map:
                raise Exception(f"Somehow got unknown contig {row['contig']} but it should have been discarded earlier in the process")

            if row["contig"] not in contig_to_include:
                continue

            chromosome = known_contig_to_chrom_map[row["contig"]]

            # note we use the 'index' field as an id and then match it back when we rejoin the VEP output with the original counts
            new_vcf_line = f"{chromosome}\t{row['position']}\tid{row['index']}\t{row['ref']}\t{row['alt']}\t.\t.\n"

            input_vcf.write(new_vcf_line)

    count = df.select(pl.len()).item()

    print(f"Created VCF at {vcf_name} of {count} Parquet variants")

    return vcf_name


def vep_json_to_parquet(docker_client: docker.DockerClient, vcf_name: str, assembly_name: str):
    """
    Process the named VCF (in the working folder) through VEP via Docker and then convert the JSONL
    output into a new dataframe of VEP specific information.

    :param docker_client:
    :param vcf_name:
    :param assembly_name:
    :return:
    """
    vep_data_folder = os.path.abspath(VEP_FOLDER)
    working_folder = os.path.abspath(WORKING_FOLDER)

    output_json_name = "vep_output.jsonl"

    docker_client.containers.run(
        "ensemblorg/ensembl-vep:release_113.4",
        f"vep --cache --offline --format vcf --safe --json --protein --assembly {assembly_name} --check_existing --canonical --af_gnomade --af_gnomadg --protein --hgvs --force_overwrite \
          --input_file /working/{vcf_name} \
          --output_file /working/{output_json_name} ",
        volumes={
            vep_data_folder: {"bind": "/data", "mode": "ro"},
            working_folder: {"bind": "/working", "mode": "rw"},
        },
        remove=True,
    )

    print(f"Created JSONL at {output_json_name}")

    # we construct a dataframe holding all the VEP data for each variant
    vep_with_index_schema = pl.Schema(indexed_record_fields | vep_record_fields)
    vep_df = pl.DataFrame(schema=vep_with_index_schema, strict=True)

    # we are going the stage the JSON data in a python array and then convert to Parquet
    # python arrays become incredibly slow when they become large - so we need to chunk the
    # writing out of the frames
    vep_output_json = []

    with open(os.path.join(WORKING_FOLDER, output_json_name), "r") as vep_json:
        for line in vep_json:
            try:
                json_line = json.loads(line)
            except json.decoder.JSONDecodeError as e:
                print("JSON parse error of VEP output line")
                print(line)
                raise e

            vep_output_json.append(json_line)

            index = int(json_line["id"][2:])

            json_line["index"] = index

            # we precompute some "sets" just because it is easier for polars to search/display
            consequences = (
                json_line["transcript_consequences"]
                if "transcript_consequences" in json_line
                else []
            )

            json_line["gene_id_set"] = list(
                set(map(lambda x: x["gene_id"], consequences))
            )
            json_line["transcript_id_set"] = list(
                set(map(lambda x: x["transcript_id"], consequences))
            )

            # we need to rejig the colocated variants data because it is otherwise a bit hard to work with in parquet
            colocated = (
                json_line["colocated_variants"]
                if "colocated_variants" in json_line
                else []
            )
            new_colocated = []

            for c in colocated:
                if "allele_string" in c:
                    if c["allele_string"] == "COSMIC_MUTATION":
                        continue

                new_colocated.append(c)

                if "frequencies" in c:
                    keys = c["frequencies"].keys()

            json_line["colocated_variants"] = new_colocated

            if index % 100000 == 0:
                print(f"Stacking data frame chunk at index {index}")
                # print(json.dumps(json_line, indent=4))
                vep_df = vep_df.vstack(
                    pl.DataFrame(
                        vep_output_json, schema=vep_with_index_schema, strict=True
                    )
                )
                vep_output_json.clear()

        print(f"Final stack of data frame chunk at index {index}")
        vep_df = vep_df.vstack(
            pl.DataFrame(
                vep_output_json, schema=vep_with_index_schema, strict=True
            )
        )
        vep_output_json.clear()

    print(f"Created VEP data frame of estimates {round(vep_df.estimated_size('mb'))} mb of data")

    return vep_df


def main():
    client = docker.from_env()
    client.ping()

    # create a data frame of all the data from the labs
    variants_df = aggregate(sources)

    print(f"Working in folder {WORKING_FOLDER}/")

    # create an aggregate VCF in the working folder and return its name (note the name is just the filename, not the full path)
    vcf_37_name = create_aggregate_vcf(variants_df, "vcf_37.vcf", known_37_contigs_list)
    vcf_38_name = create_aggregate_vcf(variants_df, "vcf_38.vcf", known_38_contigs_list)

    # take the aggregate VCF and pass it through VEP and then back into a parquet dataframe
    vep_37_df = vep_json_to_parquet(client, vcf_37_name, "GRCh37")
    vep_38_df = vep_json_to_parquet(client, vcf_38_name, "GRCh38")

    vep_all_df = vep_37_df.vstack(vep_38_df)

    # example_df = (
    #    variants_df.drop("index")
    #    .with_columns(labs_contributing_count=pl.col(labs_contributing_name).list.len())
    #    .drop(labs_contributing_name)
    #)
    #print(example_df)
    # variants_df.write_parquet(os.path.join(WORKING_FOLDER, "variants.parquet"))
    # print(vep_df)

    # vep_df.write_parquet(os.path.join(WORKING_FOLDER, "vep.parquet"))

    # this actually requires the most memory and is prone to failure
    all_df = pl.concat([variants_df, vep_all_df], how="align").drop("index")

    all_df.write_parquet("variant-counts-aggregate.parquet")

    print(all_df)


if __name__ == "__main__":
    main()


