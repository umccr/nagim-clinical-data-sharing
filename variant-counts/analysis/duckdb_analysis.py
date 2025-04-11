import posixpath
from typing import List

import duckdb

from common.vcf_aggregate_counts_vep_parquet_types import labs_contributing_count_name


def do_duckdb_analysis(bucket: str, contigs: List[str], geneid):

    con = duckdb.connect(database = ":memory:")

    # setup duckdb with some sensible defaults for using S3
    con.execute("SET memory_limit = '16GB';")
    con.install_extension("aws")
    con.execute("CREATE OR REPLACE SECRET secret (TYPE s3, REGION 'ap-southeast-2', PROVIDER credential_chain);")

    # this is the format for how we tell duckdb to select the *entire* parquet hive
    scan_path = posixpath.join("s3://" + bucket, "aggregate-counts", "latest-with-vep/*/*.parquet")

    # here however we select down into the contigs of interest - the duckdb engine
    # pushes these predicates down so that only the relevant files for contigs are even looked at
    con.execute(f"""
        CREATE TABLE combined AS SELECT * FROM '{scan_path}' WHERE contig IN $contigs;
    """, {
        "contigs": contigs
    })

    # do some SQL from the combined table into a new one with just our gene of interest
    # and with some of our nested fields expanded
    con.execute("""
        CREATE TABLE gene AS SELECT contig, position, ref, alt, hom_count, het_count, labs_contributing_count, unnest(transcript_consequences, recursive := true)
        FROM combined
        WHERE list_contains(gene_id_set, $geneid)
    """, {
        "geneid": geneid
    })

    # now do analysis on the gene data
    con.execute(f"""
        SELECT *
        FROM gene
        WHERE {labs_contributing_count_name} > 1 AND
                impact IN ['MODERATE', 'HIGH']
        ORDER BY impact DESC
    """)

    for x in con.fetchall():
        print (x)
