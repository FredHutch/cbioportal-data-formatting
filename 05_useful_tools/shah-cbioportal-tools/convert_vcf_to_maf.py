import os
import vcf
import yaml

from utils import OpenFile as open
from utils import run_cmd
from utils import run_in_gnu_parallel


def get_vcf_header(vcf_files):
    with open(vcf_files[0], 'rt') as invcf:
        header = []
        for line in invcf:
            if '##INFO' in line or '##FORMAT' in line:
                continue

            if line.startswith('##'):
                header.append(line.strip())
            elif line.startswith('#'):
                line = '\t'.join(line.strip().split()[:8])
                header.append(line)
            else:
                break

    return header


def get_vcf_data(vcf_files, pr_threshold=0.8, qss_threshold=20):
    output = {}
    for vcf_file in vcf_files:
        reader = vcf.Reader(filename=vcf_file)
        for record in reader:
            chrom = str(record.CHROM)
            pos = str(record.POS)
            ref = str(record.REF)
            qual = record.QUAL
            fltr = record.FILTER

            if 'PR' in record.INFO and record.INFO['PR'] < pr_threshold:
                continue
            if 'QSS' in record.INFO and record.INFO['QSS'] < qss_threshold:
                continue
            if fltr:
                assert len(fltr) == 1
                fltr = fltr[0]

            fltr = str(fltr) if fltr else 'PASS'
            qual = str(qual) if qual else '.'

            ref_count = 'NA'
            alt_count = 'NA'
            for sample in record.samples:
                if sample.sample == 'NORMAL':
                    sample_data = sample.data._asdict()
                    if 'RC' in sample_data and 'AC' in sample_data:
                        ref_count = str(sample_data['RC'])
                        alt_count = str(sample_data['AC'])

            for alt in record.ALT:
                key = (chrom, pos, ref, str(alt))
                value = ((qual, fltr), (ref_count, alt_count))
                if key not in output or output[key][-1][0] == 'NA':
                    output[key] = value
    return output


def write_vcf(output, vcf_files, data, tempdir, sample_id):
    temp_output = os.path.join(tempdir, '{}.vcf'.format(sample_id))

    with open(temp_output, 'wt') as outfile:
        header = get_vcf_header(vcf_files)

        for line in header:
            outfile.write(line + '\n')

        for key, key_data in data.items():
            chrom, pos, ref, alt = key
            outstr = (chrom, pos, '.', ref, alt) + key_data[0] + ('.',)
            outstr = '\t'.join(outstr) + '\n'
            outfile.write(outstr)

    sort_vcf_file(temp_output, output)


def write_allele_counts(output, vcf_data):
    with open(output, 'wt') as outfile:
        header = ['chrom', 'coord', 'ref', 'alt', 'n_ref_count', 'n_alt_count']
        header = '\t'.join(header) + '\n'
        outfile.write(header)
        for key, key_data in vcf_data.items():
            outstr = key + key_data[1]
            outstr = '\t'.join(outstr) + '\n'
            outfile.write(outstr)


def generate_mafs(vcf_files, tempdir, maf_outputs, vcf_outputs):
    ref_fasta = os.path.join('/vcf2maf/cache/', 'homo_sapiens', '99_GRCh37', 'Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz')
    filter_vcf = os.path.join('/vcf2maf/cache/', 'ExAC_nonTCGA.r0.3.1.sites.vep.vcf.gz')

    commands = []
    for sample in vcf_files:
        maf_output = maf_outputs[sample]
        vcf_input = vcf_outputs[sample]

        cmd = [
            '/opt/local/singularity/3.3.0/bin/singularity', 'run', '--bind', '/juno/work/shah/users/vatrtwaa/vcf2maf:/vcf2maf', 'docker://docker.io/wgspipeline/vcf2maf:v0.0.1',
            'vcf2maf.pl', '--input-vcf', vcf_input, '--output-maf', maf_output,
            '--vep-path', '/usr/local/bin', '--ref-fasta', ref_fasta,
            '--filter-vcf', filter_vcf, '--vep-data', '/vcf2maf/cache/',
            '--tumor-id', sample
        ]

        commands.append(cmd)

    run_in_gnu_parallel(commands, tempdir)


def sort_vcf_file(input_vcf_file, output_vcf_file):
    cmd = ['bcftools', 'sort', '-O', 'v', '-o', output_vcf_file, input_vcf_file]
    run_cmd(cmd)


def main(yamlfile, vcf_outputs, csv_outputs, maf_outputs, tempdir):
    yamldata = load_input_yaml(yamlfile)
    vcf_files = get_vcf_files(yamldata)


    for sample, sample_vcf_files in vcf_files.items():
        vcfdata = get_vcf_data(sample_vcf_files)
        write_vcf(vcf_outputs[sample], sample_vcf_files, vcfdata, tempdir, sample)
        write_allele_counts(csv_outputs[sample], vcfdata)

    generate_mafs(vcf_files, tempdir, maf_outputs, vcf_outputs)
