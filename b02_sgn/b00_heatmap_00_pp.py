import pandas as pd
from pathlib import Path
import scanpy as sc

#-------------------------------------------------------
n=70

prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/b00_heatmap_00_pp'
f_in='./out/a00_clean_04_anno/data.h5ad'
fd_gene=f'{prj}/b00_steroid/out/b00_de_02_clean'
l_cell=['Type 1A', 'Type 1B', 'Type 1C', 'Type 2']

#-------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
l_fname=list(Path(fd_gene).glob('*.csv'))

#-------------------------------------------------------
def mainf(fname, df):
	name=Path(fname).stem
	#load
	df_gene=pd.read_csv(fname, index_col=0)	
	df_gene=df_gene.drop_duplicates(subset=['gene'])
	df_gene=df_gene.loc[df_gene['gene'].isin(df.index), :]
	#get genes
	l_up=df_gene['gene'].tolist()[0:n]
	l_down=df_gene['gene'].tolist()[::-1][0:n]
	#make df
	df_up=df.reindex(l_up)
	df_down=df.reindex(l_down)
	df_up.to_csv(f'{fd_out}/{name}_up.csv')
	df_down.to_csv(f'{fd_out}/{name}_down.csv')
	return


#######################################################################
#make exp df
ada=sc.read(f_in)
df=pd.DataFrame(ada.raw.X, index=ada.obs.index, columns=ada.raw.var.index)
df=df.merge(ada.obs.loc[:, ['anno']], left_index=True, right_index=True)

#filter and sort
df=df.loc[df['anno'].isin(l_cell), :]
df['anno']=pd.Categorical(df['anno'], categories=l_cell, ordered=True)
df=df.sort_values('anno')

#save cells
dfi=df.loc[:, ['anno']].copy()
dfi.to_csv(f'{fd_out}/cell.csv')

#pp heatmap df
df=df.drop('anno', axis=1).T
df=df.loc[df.sum(axis=1)>0, :].copy()

for fname in l_fname:
	mainf(fname, df)

