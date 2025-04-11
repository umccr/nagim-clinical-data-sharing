#!/usr/bin/env -S uv run --script

from typing import Tuple, List

import polars as pl

from aggregator.lab_data_read_and_normalise import retrieve
from common.folders import VARIANT_COUNTS_INTERNAL_HIVE
from common.sources import lab_sources
from common.vcf_aggregate_counts_vep_parquet_types import (
    coord_columns,
    lab_submitted_record_fields,
    lab_submitted_source_fields,
    labs_contributing_name,
    hom_count_name,
    het_count_name,
    source_name, contig_name,
)


def generate_internal(sources: List[Tuple[str,str,str]]):
    """
    Aggregate data from source labs into an internal parquet structure
    for further analysis.

    :param sources: a list of tuples of (short name, bucket, path)
    :return: a DataFrame of aggregated data
    """
    lab_combined = pl.DataFrame(
        schema=pl.Schema(lab_submitted_record_fields | lab_submitted_source_fields)
    )

    for lab_source in sources:
        print(lab_source[0].upper())
        print("---------------------")

        lab_data, lab_msgs = retrieve(
           lab_source[0], lab_source[1], lab_source[2], False, None)

        # example limits for testing
        #lab_data, lab_msgs = retrieve(
        #    lab_source[0], lab_source[1], lab_source[2], False, 5000)
        #lab_data, lab_msgs = retrieve(
        #    lab_source[0], lab_source[1], lab_source[2], False, "NC_000019.10")

        # output some useful warning messages related to each labs data
        for m in lab_msgs:
            print(f"  {m}")
        print("")

        lab_combined = lab_combined.vstack(lab_data)

    print(lab_combined.describe())

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


def main():
    # create a data frame of all the data from the labs
    variants_df = generate_internal(lab_sources)

    # this file/partition has which lab contributed to each variant - so is considered "internal"
    # the processing
    variants_df.write_parquet(VARIANT_COUNTS_INTERNAL_HIVE, partition_by=[contig_name])

    print(variants_df)


if __name__ == "__main__":
    main()
