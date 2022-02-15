import pandas as pd
import scanpy as sc
from pathlib import Path

#-------------------------------------------
fd_out='./out/b02_violin_00_pp'
f_in='./out/a00_clean_04_anno/data.h5ad'

l_gene=['Nr3c2', 'Cacna1d', 'Nr3c1']
l_cell=['Type 1A', 'Type 1B', 'Type 1C', 'Type 2']

#-------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
ada=sc.read(f_in)

##############################################################
ada_tmp=ada[ada.obs['anno'].isin(l_cell), :].copy()
df=pd.DataFrame(ada.raw.X, index=ada.obs.index, columns=ada.raw.var.index)

df=df.loc[:, l_gene]
df['anno']=ada_tmp.obs['anno']
df.to_csv(f'{fd_out}/data.csv')

print(df)
