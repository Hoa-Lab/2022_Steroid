import pandas as pd
import scanpy as sc
from pathlib import Path

#-------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/b02_violin_00_pp'
f_in=f'{prj}/a00_raw/data/dev_kelly/p7.h5ad'

l_gene=['Nr3c2', 'Cacna1d', 'Nr3c1']
l_cell=['IHC', 'OHC', 'Deiter', 'Pillar']

#-------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
ada=sc.read(f_in)

##############################################################
ada_tmp=ada[ada.obs['anno'].isin(l_cell), :].copy()
df=pd.DataFrame(ada.X, index=ada.obs.index, columns=ada.var.index)
df=df.loc[:, l_gene]
df['anno']=ada_tmp.obs['anno']
df.to_csv(f'{fd_out}/data.csv')
