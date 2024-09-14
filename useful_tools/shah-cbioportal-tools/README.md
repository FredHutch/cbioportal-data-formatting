## cBioPortal Copy Number Data Formatting Tools

### generate_outputs.py

Code that takes four files as input:

1. genenames.org custom text file download with Approved symbol (HUGO), NCBI Gene ID (Entrez Gene ID), and Ensembl gene ID: `custom.txt`
2. a .gtf text file containing human gene information (gene start, end, and id information is used): `Homo_sapiens.GRCh37.73.gtf` (not available in the repo due to GitHub file size constraints)
3. Integrative Genomics Viewer segments text file: `igv_segs.txt`
4. TITAN segments text file: `titan_segs.txt`

and returns four text files:

1. log (median log ratio) segment data
2. gistic format gene data
3. integer segment data
4. integer gene data

### merge_outputs.py

Code that takes a directory of gistic format gene data OR integer gene data AND/OR log segment data AND/OR .maf text files and outputs a single text file with their contents merged.

### containerization

We've decided to use [vcf2maf](https://github.com/mskcc/vcf2maf) and [ensembl-vep](https://github.com/Ensembl/ensembl-vep) for our .vcf to .maf conversion needs.
Conversion has been tested with Docker:

```
docker run -it --rm \
-v /home/spenca/vcf2maf_input:/input \
-v /home/spenca/vcf2maf_output:/output \
-v /home/spenca/cache:/cache \
quay.io/biocontainers/vcf2maf:1.6.17--2 \
vcf2maf.pl \
--input-vcf /vcf2maf/input/SPECTRUM-WGS-OV-007_museq_filtered.vcf \
--output-maf /vcf2maf/output/test.maf \
--vep-path /usr/local/bin \
--ref-fasta /vcf2maf/cache/homo_sapiens/99_GRCh37/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz \
--filter-vcf /vcf2maf/cache/ExAC_nonTCGA.r0.3.1.sites.vep.vcf.gz \
--vep-data /vcf2maf/cache/ \
--tumor-id SPECTRUM-WGS-OV-007
```

as well as Singularity:

```
singularity run --bind /juno/work/shah/svatrt/vcf2maf:/vcf2maf \
docker://quay.io/biocontainers/vcf2maf:1.6.17--2 \
vcf2maf.pl \
--input-vcf /vcf2maf/input/SPECTRUM-WGS-OV-007_museq_filtered.vcf \
--output-maf /vcf2maf/output/test.maf \
--vep-path /usr/local/bin \
--ref-fasta /vcf2maf/cache/homo_sapiens/99_GRCh37/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz \
--filter-vcf /vcf2maf/cache/ExAC_nonTCGA.r0.3.1.sites.vep.vcf.gz \
--vep-data /vcf2maf/cache/ \
--tumor-id SPECTRUM-WGS-OV-007
```
