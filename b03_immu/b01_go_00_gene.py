import pandas as pd
import scanpy as sc
from pathlib import Path

#-------------------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/b01_go_00_gene'
f_ada=f'{prj}/a00_raw/data/immu_maddie/data.h5ad'
fd_gene=f'{prj}/b00_steroid/out/b00_de_02_clean'

#-------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
l_fname=list(Path(fd_gene).glob('*.csv'))

#get scRNA genes
ada=sc.read(f_ada)
l_all=ada.raw.var.index.tolist()

#################################################################
for fname in l_fname:
	name=Path(fname).stem
	df=pd.read_csv(fname, index_col=0)

	#up
	dfi=df.loc[df['logfc']>1, :].copy()
	dfi=dfi.drop_duplicates(['gene'])
	l_gene=[i for i in dfi['gene'] if i in l_all]
	Path(f'{fd_out}/{name}__up.txt').write_text('\n'.join(l_gene))

	#down
	dfi=df.loc[df['logfc']<-1, :].copy()
	dfi=dfi.drop_duplicates(['gene'])
	l_gene=[i for i in dfi['gene'] if i in l_all]
	Path(f'{fd_out}/{name}__down.txt').write_text('\n'.join(l_gene))	
