#!/usr/bin/env -S uv run --script

from analysis.duckdb_analysis import do_duckdb_analysis
from analysis.polars_analysis import do_polars_analysis
from common.reference_data_36_contigs import known_36_chrom_to_contig_map
from common.reference_data_37_contigs import known_37_chrom_to_contig_map
from common.reference_data_38_contigs import known_38_chrom_to_contig_map


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("chr")
    parser.add_argument("geneid")
    args = parser.parse_args()

    # locate the contig for the passed in chromosome
    contig_list = []

    if args.chr in known_36_chrom_to_contig_map:
        contig_list.append(known_36_chrom_to_contig_map[args.chr])
    if args.chr in known_37_chrom_to_contig_map:
        contig_list.append(known_37_chrom_to_contig_map[args.chr])
    if args.chr in known_38_chrom_to_contig_map:
        contig_list.append(known_38_chrom_to_contig_map[args.chr])

    if len(contig_list) == 0:
        raise Exception(f"No contigs found for the chromosome argument '{args.chr}'")

    do_duckdb_analysis(args.bucket, contig_list, args.geneid)
    do_polars_analysis(args.bucket, contig_list, args.geneid)


if __name__ == "__main__":
    main()
