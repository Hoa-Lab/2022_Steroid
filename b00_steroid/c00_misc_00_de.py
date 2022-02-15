import pandas as pd
import multiprocessing as mp
from pathlib import Path
import re

#------------------------------------------------------------
fd_out='./out/c00_misc_00_de'
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
		logfc=row['logFC']
		AveExpr=row['AveExpr']
		t=row['t']
		pval=row['P.Value']
		adp=row['adj.P.Val']
		b=row['B']
		l_gene=row['Gene'].split(' /// ')
		for gene in l_gene:
			l_data.append((probe, gene, logfc, AveExpr, t, pval, adp, b))
	dfi=pd.DataFrame(l_data, columns=['probe', 'Gene', 'logFC', 'AveExpr', 't', 'P.Value', 'adj.P.Val', 'B'])
	return dfi
	
	
def mainf(fname):
	#load
	name=Path(fname).stem
	df=pd.read_csv(fname, index_col=0)
	df.index.name='Probe'
	
	#add gene
	df=df.merge(df_anno, left_index=True, right_index=True)
	df=clean_probe(df)	
	df.to_csv(f'{fd_out}/{name}.csv', index=False)
	return


##########################################################################
with mp.Pool() as p:
	p.map(mainf, l_fname)


