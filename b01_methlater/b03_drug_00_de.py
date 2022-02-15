import pandas as pd
import scanpy as sc
from pathlib import Path

#--------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'

fd_out='./out/b03_drug_00_de'
fd_in=f'{prj}/b00_steroid/out/b00_de_02_clean'
f_ada='./out/a00_clean_00_load/data.h5ad'
fd_drug=f'{prj}/a00_raw/drug'

#############################################################
Path(fd_out).mkdir(exist_ok=True, parents=True)
ada=sc.read(f_ada)
l_fname=list(Path(fd_in).glob('*.csv'))

#--------------------------------------------
#all genes
l_all=ada.raw.var.index.tolist()

#drug
df_drug=pd.read_csv(f'{fd_drug}/drug.csv', index_col=0)
df_drug.index=df_drug.index.str.capitalize()
df_rep=pd.read_csv(f'{fd_drug}/repurp.csv', index_col=0)
df_rep.index=df_rep.index.str.capitalize()

#main
for fname in l_fname:
    name=Path(fname).stem
    df=pd.read_csv(fname, index_col=0)
    
    #filter
    df=df.loc[df['pval']<0.05, :]
    df=df.set_index('gene')
    df=df.loc[~df.index.duplicated()]
    
    #drug
    df0=df.merge(df_drug, left_index=True, right_index=True)
    df1=df.merge(df_rep, left_index=True, right_index=True)
    df0=df0.sort_values('logfc', ascending=False)
    df1=df1.sort_values('logfc', ascending=False)
    
    #filter genes
    df0=df0.loc[df0.index.isin(l_all), :]
    df1=df1.loc[df1.index.isin(l_all), :]
    
    #save
    df0.to_csv(f'{fd_out}/{name}_drug.csv')
    df1.to_csv(f'{fd_out}/{name}_repurp.csv')

    
