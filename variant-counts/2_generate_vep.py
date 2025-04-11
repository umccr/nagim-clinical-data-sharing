#!/usr/bin/env -S uv run --script

import json
import os
from os.path import exists
from typing import List, Tuple
from timeit import default_timer as timer

import docker
import polars as pl

from common.folders import VEP_FOLDER, WORKING_FOLDER, VARIANT_COUNTS_INTERNAL_HIVE, VARIANT_COUNTS_VEP_HIVE
from common.known_contigs import known_contig_to_chrom_map, known_37_contigs_list, known_38_contigs_list
from common.vcf_aggregate_counts_vep_parquet_types import (
    indexed_record_fields,
    vep_record_fields, contig_name,
)


def create_vcf_from_variants(df: pl.DataFrame, vcf_name: str, contig_to_include: List[str]) -> Tuple[str, int]:
    """
    Create a VCF file from records in our variant count data frame. Has the minimal information possible
    for a VCF so we can pass it in bulk to VEP. Has no other grander purpose (as a VCF) than that.

    :param df: the aggregate DataFrame of variants
    :param vcf_name: the name of the VCF file to create in the working folder
    :param contig_to_include: a list of contigs to include (so we can filter for different reference genomes)
    :return: the name of the VCF we created and the count of how many variants in the VCF
    """
    export_count = 0

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

            export_count += 1

    return vcf_name, export_count


def vep_json_to_parquet(docker_client: docker.DockerClient, vcf_name: str, assembly_name: str) -> pl.DataFrame:
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

    # see https://asia.ensembl.org/info/docs/tools/vep/script/vep_options.html
    docker_client.containers.run(
        "ensemblorg/ensembl-vep:release_113.4",
        " ".join([
            "vep",
            # instruct VEP not to download reference data - we expect it all to be present in /data
            "--cache",
            "--offline",
            # safe tells it to fail if plugins fail
            "--safe",
            # we don't use the stats so don't generate
            "--no_stats",
            # the input format we have chosen to send to VEP is VCF
            "--format",
            "vcf",
            # we want VEP to output all its information as lines of JSON
            "--json",
            # all our data is temporary so happy to overwrite
            "--force_overwrite",
            "--fork",
            "6",
            # we need to be able to handle either 37 or 38 data
            "--assembly",
            assembly_name,
            "--protein",
            "--check_existing",
            "--canonical",
            # include allele frequency from Genome Aggregation Database (gnomAD) exome populations
            "--af_gnomade",
            # include allele frequency from Genome Aggregation Database (gnomAD) genome populations
            "--af_gnomadg",
            "--protein",
            "--hgvs",
            "--input_file",
            f"/working/{vcf_name}",
            "--output_file",
            f"/working/{output_json_name}"

        ]),
        volumes={
           vep_data_folder: {"bind": "/data",  "mode": "ro"},
           working_folder: {"bind": "/working", "mode": "rw"},
        },
        remove=True,
    )

    print(f"Created JSONL at {output_json_name} via VEP docker")

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

            if index % 10000 == 0:
                # print(f"Stacking data frame chunk at index {index}")
                # print(json.dumps(json_line, indent=4))
                vep_df = vep_df.vstack(
                    pl.DataFrame(
                        vep_output_json, schema=vep_with_index_schema, strict=True
                    )
                )
                vep_output_json.clear()

        # print(f"Final stack of data frame chunk at index {index}")
        vep_df = vep_df.vstack(
            pl.DataFrame(
                vep_output_json, schema=vep_with_index_schema, strict=True
            )
        )
        vep_output_json.clear()

    return vep_df


def main():
    client = docker.from_env()
    client.ping()

    # load our previously created variant counts from all the labs
    variants_df = pl.read_parquet(VARIANT_COUNTS_INTERNAL_HIVE, hive_partitioning=True)

    print(f"Working in folder {WORKING_FOLDER}/")

    def process_contig(c: str, ref: str):
        # a sneaky test to see if we have already created this partition for this contig
        # mainly because we were having connection issues during the *long* VEP runs so we need to be
        # able to safely restart
        if exists(VARIANT_COUNTS_VEP_HIVE + f"contig={c}/00000000.parquet"):
            print(f"{" ":6} : Skipping {c} because a parquet for it already exists")
            return

        start_vcf = timer()

        vcf_name, vcf_count = create_vcf_from_variants(variants_df, f"{c}.vcf", [c])

        end_vcf = timer()

        print(f"{round(end_vcf - start_vcf):6}s: Created VCF data {vcf_name} of {vcf_count} variants")

        start_vep = timer()

        # take the genome specific VCF and pass it through VEP and then back into a parquet dataframe
        vep_df = vep_json_to_parquet(client, vcf_name, ref)

        end_vep = timer()

        print(f"{round(end_vep - start_vep):6}s: Created VEP data frame of approximately {round(vep_df.estimated_size('mb'))} mb of data")

        # note here we are telling it the column name to partition by - not passing in the actual current
        # contig 'c' (write_parquet will handle that)
        vep_df.write_parquet(VARIANT_COUNTS_VEP_HIVE, partition_by=[contig_name])

    # for memory saving reasons we process each contig separately (VCF -> VEP output parqet)
    # but we note that we need to use different reference data for 37 v 38 so we call them
    # separately
    for contig in known_37_contigs_list:
        process_contig(contig, "GRCh37")

    for contig in known_38_contigs_list:
        process_contig(contig, "GRCh38")


if __name__ == "__main__":
    main()


