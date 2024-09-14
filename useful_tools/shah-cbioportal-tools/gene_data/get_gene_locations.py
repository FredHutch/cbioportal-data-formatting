import requests
import pandas as pd


hgnc_file = 'hugo_genes.tsv.gz'
gtf_file = 'Homo_sapiens.GRCh37.73.gtf.gz'
chromosomes = [str(a) for a in range(1, 23)] + ['X', 'Y']


def read_gene_data(gtf):
    data = pd.read_csv(
        gtf,
        delimiter='\t',
        names=['chromosome', 'gene_start', 'gene_end', 'info'],
        usecols=[0,3,4,8],
        converters={'chromosome': str},
    )

    def extract_info(info):
        info_dict = {}
        for a in info.split('; '):
            k, v = a.split(' ')
            info_dict[k] = v.strip(';').strip('"')
        return info_dict
    
    data['info'] = data['info'].apply(extract_info)
    data['gene_id'] = data['info'].apply(lambda a: a['gene_id'])
    data['gene_name'] = data['info'].apply(lambda a: a['gene_name'])

    data = data.groupby(['chromosome', 'gene_id', 'gene_name']).agg({'gene_start':'min', 'gene_end':'max'}).reset_index()

    return data


genes = read_gene_data(gtf_file)
genes = genes.merge(pd.DataFrame({'chromosome': chromosomes}))

# Remove duplicates by randomly choosing one gene per gene name
genes = genes.drop_duplicates(subset=['gene_name'])

genes_page_0 = requests.get('https://www.cbioportal.org/api/genes')
genes_page_1 = requests.get('https://www.cbioportal.org/api/genes?pageNumber=1')
gene_request = genes_page_0.json() + genes_page_1.json()

cbio_genes = pd.DataFrame(gene_request)
cbio_genes.rename(columns={'hugoGeneSymbol': 'Hugo_Symbol', 'entrezGeneId': 'Entrez_Gene_Id'}, inplace=True)
cbio_genes['Hugo_Symbol'] = cbio_genes['Hugo_Symbol'].str.upper()
cbio_genes['Entrez_Gene_Id'] = cbio_genes['Entrez_Gene_Id'].astype(int)

hgnc = pd.read_csv(hgnc_file, delimiter='\t', dtype=str)
hgnc = hgnc[['Approved symbol', 'Alias symbol', 'Previous symbol']].drop_duplicates()

# Ensembl contains approved hugo symbol
approved = (
    genes
    .rename(columns={'gene_name': 'Hugo_Symbol'})
    .merge(cbio_genes).set_index('Hugo_Symbol'))

# Ensembl contains alias symbol
aliased = (
    genes
    .rename(columns={'gene_name': 'Alias symbol'})
    .merge(hgnc)
    .rename(columns={'Approved symbol': 'Hugo_Symbol'})
    .merge(cbio_genes)
    .set_index('Hugo_Symbol'))

# Ensembl contains previous symbol
previous = (
    genes
    .rename(columns={'gene_name': 'Previous symbol'})
    .merge(hgnc)
    .rename(columns={'Approved symbol': 'Hugo_Symbol'})
    .merge(cbio_genes)
    .set_index('Hugo_Symbol'))

gene_locations = cbio_genes.set_index('Hugo_Symbol')
gene_locations['chromosome'] = ''
gene_locations['gene_start'] = -1
gene_locations['gene_end'] = -1

# Previous symbols last
gene_locations.loc[previous.index, ['chromosome', 'gene_start', 'gene_end']] = previous[['chromosome', 'gene_start', 'gene_end']]

# Aliased second
gene_locations.loc[aliased.index, ['chromosome', 'gene_start', 'gene_end']] = aliased[['chromosome', 'gene_start', 'gene_end']]

# Approved first
gene_locations.loc[approved.index, ['chromosome', 'gene_start', 'gene_end']] = approved[['chromosome', 'gene_start', 'gene_end']]

gene_locations = gene_locations.reset_index()
gene_locations = gene_locations.query('gene_start > 0')

gene_locations.to_csv('gene_locations.csv.gz', index=False)
