import pandas as pd
import scanpy as sc
import anndata as ad
from pathlib import Path
import re

#----------------------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/a00_clean_00_load'
f_in=f'{prj}/a00_raw/data/sgn_goodrich/GSE114997_Shrestha_normalized_counts.csv'

#----------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
df=pd.read_csv(f_in, index_col=0)
	
	
#################################################################
#clean
df.columns=[f'cell_{i}' for i in df.columns]
df=df.T

#make ada
obs=pd.DataFrame(df.index)
obs.columns=['cell']
obs=obs.set_index('cell')

var=pd.DataFrame(df.columns)
var=var.set_index('Gene')

ada=ad.AnnData(df.values, obs=obs, var=var)
ada.write(f'{fd_out}/ada.h5ad')











