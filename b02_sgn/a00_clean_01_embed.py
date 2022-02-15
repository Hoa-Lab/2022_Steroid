import scanpy as sc
import pandas as pd
from pathlib import Path

#-------------------------------------------------------
fd_out='./out/a00_clean_01_embed'
f_in='./out/a00_clean_00_load/ada.h5ad'

#-------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
ada=sc.read(f_in)

#####################################################################
#hvg
sc.pp.filter_genes(ada, min_cells=3)  #must filter 0s before call HVG
sc.pp.highly_variable_genes(ada, n_top_genes=2000, flavor='cell_ranger', inplace=True)
ada.raw=ada
ada=ada[:, ada.var.highly_variable]

#embed
sc.tl.pca(ada, svd_solver='arpack')
sc.pp.neighbors(ada)
sc.tl.umap(ada, n_components=2, random_state=42)

ada.write(f'{fd_out}/ada.h5ad')
