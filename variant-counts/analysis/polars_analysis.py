import posixpath
from typing import List

import polars as pl

from common.vcf_aggregate_counts_vep_parquet_types import contig_name, \
    labs_contributing_count_name, combined_record_schema


def do_polars_analysis(bucket: str, contigs: List[str], geneid):

    # needs to be slash terminated to tell polars we are looking at a Hive folder
    scan_path = posixpath.join("s3://" + bucket, "aggregate-counts", "latest-with-vep") + "/"

    # bring in the variants for the given contigs
    vep_variants_df = (
        pl.scan_parquet(
            scan_path,
            schema=combined_record_schema,
            hive_partitioning=True,
            storage_options={"region": "ap-southeast-2"}
        )
        .filter(pl.col(contig_name).is_in(contigs))
        .collect()
    )

    # perform a sample "analysis" (just do some filtering and re-org of columns)
    with (pl.Config() as cfg):
        cfg.set_tbl_width_chars(300)
        cfg.set_tbl_cols(30)
        cfg.set_tbl_rows(6)

        # filter to only variants in the gene of interest
        vep_variants_df = vep_variants_df.filter(
            pl.col("gene_id_set").list.contains(geneid)
        )

        # example: filter for variants from more than 1 lab
        vep_variants_df = vep_variants_df.filter(pl.col(labs_contributing_count_name) > 1)

        # allele string is in both the exploded transcripts and the top-level entry - so delete from the top-level entry
        vep_variants_df = vep_variants_df.drop("allele_string")

        # explode out the 1:many relationships of the VEP annotations
        vep_variants_df = (
            vep_variants_df.explode("transcript_consequences")
            .unnest("transcript_consequences")
            .explode("colocated_variants")
            .unnest("colocated_variants")
            .filter(pl.col("canonical") == 1)
            .filter(pl.col("somatic").is_null())
            # limit to higher impact
            .filter(pl.col("impact").is_in(["MODERATE", "HIGH"]))
        )

        # example: remove columns that we are not interested in
        # vep_variants_df =
        #    vep_variants_df.drop("allele_string")

        vep_variants_df = vep_variants_df.sort("impact", descending=True)

        print(vep_variants_df)
