import pandas as pd
import multiprocessing as mp
from pathlib import Path
import re

#------------------------------------------------------------
fd_out='./out/b00_de_02_clean'
fd_in='./out/b00_de_01_de'
f_anno='./out/a01_anno_00_clean/conversion.csv'

#------------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
l_fname=list(Path(fd_in).glob('*.csv'))
df_anno=pd.read_csv(f_anno, index_col=0)

#------------------------------------------------------------
def clean_probe(dfi):
	'''some gene has label as: Snrpn /// Snurf'''
	l_data=[]
	for probe, row in dfi.iterrows():
		logfc=row['logfc']
		p=row['pval']
		l_gene=row['Gene'].split(' /// ')
		for gene in l_gene:
			l_data.append((probe, gene, logfc, p))
	dfi=pd.DataFrame(l_data, columns=['probe', 'gene', 'logfc', 'pval'])
	return dfi


def clean_gene(l_gene):
	l_gene=[i for i in l_gene if not i.startswith(('ERCC-', 'tg-', 'tg_', 'mt-', 'Rpl', 'Rps', 'Mrpl', 'n-', 'Ighv', 'Igkv', 'Ighd'))]
	l_gene=[i for i in l_gene if not re.match('^[A-Z][A-Z]', i)]
	l_gene=[i for i in l_gene if not re.match('^[a-z][0-9]', i)]
	l_gene=[i for i in l_gene if not re.match('^[a-z][a-z]', i)]
	l_gene=[i for i in l_gene if not re.match('^Mir[0-9]', i)]
	l_gene=[i for i in l_gene if not ('-ps' in i)]
	l_gene=[i for i in l_gene if not (('Rik' in i) & (not i.startswith('Rik')))]
	l_gene=[i for i in l_gene if len(i)>1]
	l_gene=[i for i in l_gene if not re.match('^Gm[0-9]', i)]
	l_gene=list(set(l_gene))
	l_gene.sort()
	return l_gene
	
	
def mainf(fname):
	#load
	name=Path(fname).stem
	df=pd.read_csv(fname, index_col=0)
	df.index.name='Probe'
	#clean & filter
	df=df.loc[:, ['logFC', 'adj.P.Val']]
	df.columns=['logfc', 'pval']
	df=df.loc[df['pval']<=0.05, :]
	#label genes
	df=df.merge(df_anno, left_index=True, right_index=True)
	df=clean_probe(df)
	#filter genes
	l_gene=clean_gene(df['gene'].tolist())
	df=df.loc[df['gene'].isin(l_gene), :]
	#save
	df=df.sort_values('logfc', ascending=False)
	df.to_csv(f'{fd_out}/{name}.csv', index=False)
	return


##########################################################################
with mp.Pool() as p:
	p.map(mainf, l_fname)


