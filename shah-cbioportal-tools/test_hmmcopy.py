import pandas as pd

from hmmcopy import calculate_gene_copy


def test_calculate_gene_copy():
    # Create some cnv data
    cnv = pd.DataFrame([{'chr': 'Y', 'start': 1, 'end': 59500000, 'width': 59500000, 'copy': 0.0657638, 'reads': 58774, 'state': 0}])

    # Create some gene data
    genes = pd.DataFrame([{'chr': 'Y', 'gene_id': 'ENSG00000012817', 'gene_start': 21865751, 'gene_end': 21906825}])

    # Create known overlap
    overlapping = pd.DataFrame([{'chr': 'Y', 'gene_id': 'ENSG00000012817', 'gene_start': 21865751, 'gene_end': 21906825, 'start': 1, 'end': 59500000, 'width': 59500000, 'copy': 0.0657638, 'reads': 58774, 'state': 0, }])

    assert overlapping.equals(calculate_gene_copy(cnv, genes))


def main():
    test_calculate_gene_copy()


if __name__ == '__main__':
    main()
    