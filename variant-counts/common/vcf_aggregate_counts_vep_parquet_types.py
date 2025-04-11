import polars as pl

#
# a set of Polars schema definitions for VCF/VEP data represented in Parquet
# in particular, this is for Parquet data holding aggregate counts of variants
#

contig_name = "contig"
contig_dtype = pl.String()

position_name = "position"
position_dtype = pl.UInt64()

ref_name = "ref"
ref_dtype = pl.String()

alt_name = "alt"
alt_dtype = pl.String()

hom_count_name = "hom_count"
hom_count_dtype = pl.UInt32()

het_count_name = "het_count"
het_count_dtype = pl.UInt32()

# when we want to collate/aggregate our data - we need a definition of which columns combine
# to make our unique variant records
coord_columns = [contig_name, position_name, ref_name, alt_name]

# the Parquet data as submitted by each lab
lab_submitted_record_fields = {
    contig_name: contig_dtype,
    position_name: position_dtype,
    ref_name: ref_dtype,
    alt_name: alt_dtype,
    hom_count_name: hom_count_dtype,
    het_count_name: het_count_dtype,
}

#
# some columns and schemas that we use internally to help aggregate the data across the labs
# (keeps track of which lab has submitted data - which we then remove before outputting)
#

# a field we add into submitted data to identify which lab this record comes from
source_name = "source"
source_dtype = pl.String()

lab_submitted_source_fields = {
    source_name: source_dtype,
}

# an array of lab source names that identify who has contributed to the count
labs_contributing_name = "labs_contributing"
labs_contributing_dtype = pl.List(pl.String())

lab_contributing_fields = {
    labs_contributing_name: labs_contributing_dtype
}

# a summary count of the number of lab sources that contributed to the count
labs_contributing_count_name = "labs_contributing_count"
labs_contributing_count_dtype = pl.UInt32()

lab_contributing_count_fields = {
    labs_contributing_count_name: labs_contributing_count_dtype
}

#
# columns and schemas for holding the additional VEP data of each variant
# NOTE: the naming and types of these fields matches the JSON output by VEP
#

transcript_consequences_dtype = pl.List(
    pl.Struct(
        {
            "impact": pl.String(),
            "gene_id": pl.String(),
            "transcript_id": pl.String(),
            "allele_num": pl.Int64(),
            "canonical": pl.Int64(),
            "cdna_start": pl.Int64(),
            "cdna_end": pl.Int64(),
            "cds_start": pl.Int64(),
            "cds_end": pl.Int64(),
            "protein_start": pl.Int64(),
            "protein_end": pl.Int64(),
            "variant_allele": pl.String(),
            "hgvsp": pl.String(),
            "hgvsc": pl.String(),
            "codons": pl.String(),
            "amino_acids": pl.String(),
            # 'strand': pl.Int8(),
            "consequence_terms": pl.List(pl.String()),
            "distance": pl.Int64(),
            #
            "protein_id": pl.String(),
        }
    )
)

colocated_variants_dtype = pl.List(
    pl.Struct(
        {
            #    "var_synonyms": pl.Stru,
            "allele_string": pl.String(),
            "id": pl.String(),
            "seq_region_name": pl.String(),
            "start": pl.UInt64(),
            "end": pl.UInt64(),
            "strand": pl.Int8(),
            "somatic": pl.Int8(),
            "clin_sig": pl.List(pl.String()),
            "phenotype_or_disease": pl.Int8(),
            # "frequencies": pl.Object(),
        }
    )
)

indexed_record_fields = {
    "index": pl.UInt32(),
}

vep_record_fields = {
    "allele_string": pl.String(),
    "most_severe_consequence": pl.String(),
    "gene_id_set": pl.List(pl.String()),
    "transcript_id_set": pl.List(pl.String()),
    "colocated_variants": colocated_variants_dtype,
    "transcript_consequences": transcript_consequences_dtype,
}

# vep_record_schema = pl.Schema(indexed_record_fields | vep_record_fields)

complete_record_schema = pl.Schema(
    lab_submitted_record_fields | lab_contributing_fields | vep_record_fields
)

combined_record_schema = pl.Schema(
    lab_submitted_record_fields | lab_contributing_count_fields | vep_record_fields
)


