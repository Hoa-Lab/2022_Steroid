import scanpy as sc
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from multiprocessing import Pool
import json

#-----------------------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/a00_clean_02_exp'
f_in='./out/a00_clean_01_embed/ada.h5ad'
f_meta=f'{prj}/a00_raw/data/sgn_goodrich/cell.json'

#----------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
ada=sc.read(f_in)

#load marker
with open(f_meta, 'r') as f:
	d_meta=json.load(f)
l_gene=[d_meta[i]['marker'] for i in d_meta.keys()]
l_gene=list(pd.core.common.flatten(l_gene))

#----------------------------------------------------------
def plt_exp(gene, f_out, ada=None, vmin=-0.5, vmax=None):
	ax=sc.pl.umap(ada, color=[gene], show=False, s=60, alpha=1, frameon=False, cmap='BuPu', vmin=vmin, vmax=vmax, use_raw=False)
	#adjust
	fig = plt.gcf()
	fig.set_size_inches((3.5, 4))
	ax.set_title(gene, fontsize=18, pad=10, weight='semibold')
	#save
	plt.tight_layout()
	plt.savefig(f_out, dpi=300)
	plt.close()	
	return


def mainf(gene):
	f_out=f'{fd_out}/{gene}.png'
	try:
		plt_exp(gene, f_out, ada=ada)
	except Exception:
		print(f'{gene} not found...')
	return

############################################################################
with Pool() as pool:
	pool.map(mainf, l_gene)




