# NAGIM clinical data sharing

Scripts and software for pilot of NAGIM clinical data sharing.

## `variant-counts`

Variants counts is a project to produce aggregate variant data across
labs.

We start in the `variant-counts` folder. As a pre-requisite we must
have

* Python 3.12+
* uv


### Running an analysis

The combined aggregate data from all labs has been computed as of April 2025 - for each lab that provided a bucket
the aggregated data has been returned into that bucket.

All data is provided as a Hive partitioned parquet table, both simply and with VEP annotations.

Simple aggregate count data can be found at

```
s3://<bucket>/aggregate-counts/latest/
```

and aggregate count data augmented with VEP annotations can be found at

```
s3://<bucket>/aggregate-counts/latest-with-vep/
```

We have provided a sample of using the data in analysis - this is using the VEP annotations to narrow
data down to a single Ensembl gene id.

For example, we can run `./4_analysis_by_gene.py <bucket> 2 ENSG00000155657`.

The analysis code contains an example in both DuckDb *and* Polars. The output is information from
the combined lab dataset - narrowed down to a single gene of interest.

It is mainly to show the way information can be manipulated in the DuckDb and Polars
tables - it is not an *actual* analysis of anything.


### Running the generation (central system only)

In addition to the usual pre-requisites - we must also have

* Docker
* Homo sapiens vep_data for both HG37 and HG38 (in a folder called `vep_data` in `variant-counts`)

We have split the operations into three phases - due to some memory
constraints and the fact we want to save partial results as we go.


#### Phase 1 - internal data (minutes)

We source data from each lab (see top of Python for a dictionary of the
labs and where the data comes from) and aggregate the counts by variant. Because
this data names which lab each variant count comes from it is considered
internal data. Each
lab that contributes to a variant gets listed in the "sources".

To run `./1_generate_internal.py`

#### Phase 2 - VEP results for each variant (hours!)

For analysis purposes we want to see what VEP has to say about each variant
we have encountered. This requires the most memory and compute - so we separate
out this process for each contig in the internal aggregate data.

To run `./2_generate_vep.py`

If the Docker client immediately fails - then for some reason Docker is not able to establish
a connection to its server. This seems to be happening on some modern Macs - where it
can't use the default unix socket.

Try (something like) `export DOCKER_HOST=unix:///Users/  your username  /.docker/run/docker.sock`


#### Phase 3 - combined data (an hour)

Finally we need to join the tables together and take out identifying information
of each lab (by computing counts of labs, rather than names of labs).

To run `./3_generate_aggregate.py`


