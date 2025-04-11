#!/usr/bin/env -S uv run --script

from gc import collect
from time import sleep
from os.path import exists

import polars as pl

from common.folders import VARIANT_COUNTS_INTERNAL_HIVE, VARIANT_COUNTS_AGGREGATE_HIVE, VARIANT_COUNTS_VEP_HIVE, \
    VARIANT_COUNTS_AGGREGATE_WITH_VEP_HIVE
from common.known_contigs import known_contigs_list
from common.vcf_aggregate_counts_vep_parquet_types import labs_contributing_name, contig_name, position_name, ref_name, \
    alt_name, hom_count_name, het_count_name, labs_contributing_count_name


def main():
    # this is the master aggregate data with *all* labs and *all* variants
    master_variants_df = pl.scan_parquet(VARIANT_COUNTS_INTERNAL_HIVE, low_memory=True, hive_partitioning=True)

    # we split the job by contig for lower memory usage - and because have the resulting
    # files split by contig is also useful
    for contig in known_contigs_list:
        if exists(VARIANT_COUNTS_AGGREGATE_HIVE + f"contig={contig}/00000000.parquet"):
            print(f"{" ":6} : Skipping {contig} because a parquet for it already exists")
            return

        # we are only interested in joining *this* contig variants to the VEP one
        # so we set a filter
        # NOTE: these are both in scan/streaming mode so will not actually load data until
        # later collect() steps
        variants_df = master_variants_df.filter(pl.col(contig_name).eq(contig))
        vep_df = (pl.scan_parquet(VARIANT_COUNTS_VEP_HIVE, low_memory=True)
                    .filter(pl.col(contig_name).eq(contig))
                 )

        print(f"Start aligning for contig {contig}")

        # we join the original variants (our hom and het counts) with the generated VEP data
        # note that the right table (vep) CANNOT have "index" values that didn't occur in the left table
        # as the indexes were all passed to VEP to make the right table
        # for that reason, we left join/align
        variants_df, vep_df= pl.align_frames(
            variants_df, vep_df, on="index", how="left"
        )

        # before we concat the frames we drop the common field - as we don't need it anyhow
        # we also collect() the frames as concat doesn't work well with streaming
        variants_df = variants_df.drop("index").collect()
        vep_df = vep_df.drop("index").collect()

        print(f"Done aligning for contig {contig}")

        # this actually requires the most memory and is prone to (silent out of memory) failure
        # (has been run successfully on an EC2 instance with 64 GiB of memory)
        all_df = pl.concat([variants_df, vep_df], how="horizontal")

        all_df = (all_df.with_columns(labs_contributing_count=pl.col(labs_contributing_name).list.len())
                        .drop(labs_contributing_name))

        print(f"Done concat with lab count added for contig {contig}")

        all_df.write_parquet(VARIANT_COUNTS_AGGREGATE_WITH_VEP_HIVE, partition_by=[contig_name])

        print(f"Done writing parquet with vep for contig {contig}")

        (all_df.select([contig_name, position_name,
                       ref_name, alt_name,
                       hom_count_name, het_count_name,
                       labs_contributing_count_name])
                .write_parquet(VARIANT_COUNTS_AGGREGATE_HIVE, partition_by=[contig_name]))

        print(f"Done writing parquet basic for contig {contig}")


        # polars has terrible out of memory handling - so we do all we can to help
        # it know when artefacts are no longer needed
        del all_df
        del variants_df
        del vep_df

        collect()

        sleep(10)

        # An example of the memory pressure part way through the combining
        # The VIRT memory slowly creeps up at about 1GiB per contig
        # RES memory seems pinned at about 24GiB and that is probably the important one
        #
        # top - 00:43:33 up 18 min,  2 users,  load average: 0.85, 0.97, 0.69
        # Tasks: 173 total,   2 running, 171 sleeping,   0 stopped,   0 zombie
        # %Cpu(s): 33.4 us,  1.0 sy,  0.0 ni, 65.5 id,  0.1 wa,  0.0 hi,  0.0 si,  0.1 st
        # MiB Mem :  31558.2 total,   3176.4 free,   8528.7 used,    712.6 buff/cache
        # MiB Swap:      0.0 total,      0.0 free,      0.0 used.  23029.5 avail Mem
        #
        #     PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
        #    4645 ubuntu    20   0   47.3g  23.1g  13752 R 100.3  74.9   6:57.39 python3
        #


if __name__ == "__main__":
    main()


