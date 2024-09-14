import click
import filecmp

from merge_outputs import merge_gistic_gene_data


# check output against baseline
@click.command()
@click.option('--file_type', type=click.Choice(['all', 'gistic_gene', 'log_seg', 'maf'], case_sensitive=False), multiple=True, default=['all'])
@click.option('--input_dir', default='test/merge_outputs/test_input/')
@click.option('--output_dir', default='test/merge_outputs/test_output/')
def main(file_type, input_dir, output_dir):
    merge_gistic_gene_data(input_dir, output_dir)

    if filecmp.cmp('test/merge_outputs/output_baseline/merged.txt', output_dir + 'merged.txt'):
        print('Merged file matches baseline.')
    else:
        print('Merged file does not match baseline!')


if __name__ == '__main__':
    main()
