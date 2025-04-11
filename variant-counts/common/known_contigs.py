# a list of known contigs of interest to the system
# other contigs encountered will be thrown out - with a warning
from common.reference_data_36_contigs import known_36_chrom_to_contig_map
from common.reference_data_37_contigs import known_37_chrom_to_contig_map
from common.reference_data_38_contigs import known_38_chrom_to_contig_map

known_38_contig_to_chrom_map = {v: k for k, v in known_38_chrom_to_contig_map.items()}
known_38_contigs_list = list(known_38_contig_to_chrom_map.keys())

known_37_contig_to_chrom_map = {v: k for k, v in known_37_chrom_to_contig_map.items()}
known_37_contigs_list = list(known_37_contig_to_chrom_map.keys())

known_36_contig_to_chrom_map = {v: k for k, v in known_36_chrom_to_contig_map.items()}
known_36_contigs_list = list(known_36_contig_to_chrom_map.keys())

# note: we are chosing to only include 37 and 38 here rather than adding in 36 (which
# we have made a contig map for just for completeness)
known_contigs_list = (
        known_38_contigs_list
        + known_37_contigs_list
)

known_contig_to_chrom_map = known_38_contig_to_chrom_map | known_37_contig_to_chrom_map
