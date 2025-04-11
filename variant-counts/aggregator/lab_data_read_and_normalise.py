from typing import Tuple, List, Optional, Union

import polars as pl
from polars import Series

from common.known_contigs import known_contigs_list
from common.vcf_aggregate_counts_vep_parquet_types import coord_columns, lab_submitted_record_fields, source_name


def retrieve(
    source: str,
    bucket_name: Optional[str],
    key_or_path: str,
    csv: bool,
    limit: Optional[Union[int, str]],
) -> Tuple[pl.DataFrame, List[str]]:
    """
    Returns the variant count data for a specific lab at a specific prefix (i.e. "2020-04-01/").
    Needs to be told whether it is expecting CSV or Parquet formatted data.
    Will then attempt to normalise the data so that the returned DataFrame is
    consistent.
    Also return a list of messages that may be important from the normalisation
    process.

    :param source: a short identifier for this source - will be added to every row in the output data frame
    :param bucket_name: a bucket name in S3 in which we are looking for data, or if none the local filesystem
    :param key_or_path: the object key to pass to look for data (trailing / means wildcard scan), or if bucket is none then the path on a local filesystem
    :param csv: whether to expect CSV or Parquet files (we use CSV for ease of test data - it only supports local filesystem)
    :param limit: if present and a string - filter to a contig, if present and an int - take the head of the files
    :return:
    """
    warning_msgs: List[str] = []

    if csv and bucket_name:
        raise ValueError("CSV mode can only run against local filesystem")

    if csv:
        if isinstance(limit, int) and limit > 0:
            df = pl.read_csv(key_or_path, has_header=True, n_rows=limit)
        else:
            df = pl.read_csv(key_or_path, has_header=True)
    else:
        if bucket_name:
            scan_path = f"s3://{bucket_name}/{key_or_path}"
        else:
            scan_path = key_or_path

        # we have some labs whose buckets do not allow scanning - so where the S3 path is specified
        # explicitly (no trailing /) - we read directly

        if key_or_path.endswith("/"):
            scan_wildcard = f"{scan_path}*.parquet"

            if isinstance(limit, int) and limit > 0:
                df = pl.scan_parquet(scan_wildcard, n_rows=limit, storage_options={"region": "ap-southeast-2"}).collect()
            else:
                df = pl.scan_parquet(scan_wildcard, storage_options={"region": "ap-southeast-2"}).collect()
        else:
            if isinstance(limit, int) and limit > 0:
                df = pl.read_parquet(scan_path, n_rows=limit, storage_options={"region": "ap-southeast-2"})
            else:
                df = pl.read_parquet(scan_path, storage_options={"region": "ap-southeast-2"})


    # note that however the loader - we have materialised the data by now (i.e. collect())
    # unless our files grow super large we easily have memory to handle this,
    # and if they do grow too large - we can pivot to using streaming polars

    wanted_columns: List[Series] = []

    # select out just the columns we want and normalise any types
    for c in df.iter_columns():
        if c.name not in lab_submitted_record_fields:
            warning_msgs.append(f"Dropped unused column '{c.name}'")
        else:
            # for some labs they produce this data as signed values
            # we correctly cast that here
            if c.dtype == pl.Int64:
                c = c.cast(pl.UInt64, strict=True)
            elif c.dtype == pl.Int32:
                c = c.cast(pl.UInt32, strict=True)

            wanted_columns.append(c)

    # bring them together and assert the new data frame matches our desired
    # schema
    df = pl.DataFrame(wanted_columns, schema=pl.Schema(lab_submitted_record_fields))

    # if selected, for debug purposes we might limit to a certain contig
    if isinstance(limit, str):
        df = df.filter((pl.col("contig") == limit))

    # we want to only keep known contigs (and warn about the ones we are throwing out)
    unknown = (
        df.filter(pl.col("contig").is_in(known_contigs_list).not_()).select("contig").unique()
    )

    for u in unknown.rows():
        warning_msgs.append(f"Dropped (one or more) rows with unknown contig '{u[0]}'")

    df = df.filter(pl.col("contig").is_in(known_contigs_list))

    # aggregate up the counts *within* all the dataset from this single source
    # as potentially the same variant might occur across different parquet files from the source
    # (maybe they have a parquet file per cohort)
    df = df.group_by(coord_columns).agg(
        pl.col("hom_count").sum(), pl.col("het_count").sum()
    )

    # might help if we know it is sorted
    df = df.sort(by=coord_columns)

    # add in a column with the name of the source - will be used for some other aggregation calculations
    df = df.with_columns(**{source_name: pl.lit(source)})

    print(
        f"The estimate is that our retrieved data contains {round(df.estimated_size('mb'))} mb of data from {df.select(pl.len()).item()} variants"
    )

    return df, warning_msgs
