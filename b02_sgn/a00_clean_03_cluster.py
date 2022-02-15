import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
from pathlib import Path

#------------------------------------------------------
res=2

fd_out='./out/a00_clean_03_cluster'
f_in='./out/a00_clean_01_embed/ada.h5ad'

#------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
ada=sc.read(f_in)

#------------------------------------------------------
def plt_clus(ada, f_out, col='leiden', title=None):
	#plot
	ax=sc.pl.umap(ada, color=[col], legend_loc='on data', s=60, alpha=1, palette='tab20', show=False, frameon=False, legend_fontsize=15, legend_fontweight='semibold')
	#adjust
	fig = plt.gcf()
	fig.set_size_inches((3.5, 4))
	ax.set_title(title, fontsize=18, pad=10, weight='semibold')
	#save
	plt.tight_layout()
	plt.savefig(f_out, dpi=300)
	plt.close()
	return


#############################################################################
#cluster
sc.tl.leiden(ada, resolution=res, random_state=42)
ada.write(f'{fd_out}/data.h5ad')

#plot
f_out=f'{fd_out}/cluster.png'
plt_clus(ada, f_out, title='SGN')
