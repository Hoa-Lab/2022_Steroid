import pandas as pd
from pathlib import Path
import scanpy as sc

#----------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/a00_clean_00_load'
f_in=f'{prj}/a00_raw/data/methlater/concat_merged.h5ad'
l_cell=['Marginal', 'Intermediate', 'Basal', 'Spindle', 'Root', 'Reissner', 'Fibrocyte', 'Macrophage']

#----------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
ada=sc.read(f_in)


##################################################################
#rename
ada.obs['anno']=ada.obs['anno'].replace(['Spindle-Root-1', 'Spindle-Root-2'], ['Root', 'Spindle'])

ada.write(f'{fd_out}/data.h5ad')
