# This file is more of a guide to how input files were more or less converted into proper cbio format

# CNVkit log2 ratio - command below might give you extra new lines
cut -f 2,6- cnv_data_0326_2020.tsv| tr -d \" | tr "\r\n" "\n" | sed "s/gene_Symbol/Hugo_Symbol/" > merged_cnvs/brain.log2_ratio.tsv

# Rsem log2 fpkm
cut -f 1,3- rna_data_0316_2020.tsv | sed -r "s/X7316./7316-/g" | tr -d \" | sed "s/gene_Symbol/Hugo_Symbol/" > merged_rsem/brain.log2_fpkm.tsv

# Protein data
cut -f 1,3- proteo_tumorall_nofilter_imputedA_03162020.tsv | sed -E "s/X7316./7316-/g" | tr -d \" | sed "s/gene_Symbol/Composite.Element.REF/" | perl -e '$h=<>;print $h; while(<>){@a = split /\t/, $_; $a[0] .= "|".$a[0]; print join("\t", @a);}' > brain.quantification.txt