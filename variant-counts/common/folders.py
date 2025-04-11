# an arbitrary local folder where we will exchange data to and from VEP/Docker
WORKING_FOLDER = "./vep_working"

# a required folder where the VEP reference data is
VEP_FOLDER = "./vep_data"

# we create a bunhc of Hive partitioned data - these
# are their folder name (with trailing slash for use with polars directly)

VARIANT_COUNTS_INTERNAL_HIVE = "variant-counts-internal/"

VARIANT_COUNTS_VEP_HIVE = "variant-counts-vep/"

VARIANT_COUNTS_AGGREGATE_HIVE = "variant-counts-aggregate/"

VARIANT_COUNTS_AGGREGATE_WITH_VEP_HIVE = "variant-counts-aggregate-with-vep/"
