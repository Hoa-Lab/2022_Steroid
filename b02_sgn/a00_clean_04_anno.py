import pandas as pd
import scanpy as sc
from pathlib import Path
import matplotlib.pyplot as plt
import json

#----------------------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/a00_clean_04_anno'
f_in='./out/a00_clean_03_cluster/data.h5ad'
f_meta=f'{prj}/a00_raw/meta/cell_sgn.json'

d_anno={'Type 1A': [2,3,5,8],
	    'Type 1B': [1,4,9],
	    'Type 1C': [0,6],
	    'Type 2': [7]}
		  
#----------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
ada=sc.read(f_in)

#load marker
with open(f_meta, 'r') as f:
	d_meta=json.load(f)
d_cmap={i:d_meta[i]['color'] for i in d_meta.keys()}

#-----------------------------------------------------
def anno_ada(ada, dic_anno, missing='Unknown'):
	ada.obs['anno']=ada.obs['leiden'].astype('int')
	#check clusters
	l_lbl=sum(dic_anno.values(), [])
	if len(l_lbl)!=len(set(l_lbl)):
		raise Exception('Duplicated Clusters')
	#pp unknown clusters
	n_clus=ada.obs['leiden'].astype('int').max()
	l_unknown=list(range(n_clus+1))
	l_unknown=[i for i in l_unknown if i not in l_lbl]	
	#anno
	for cell, l_clus in dic_anno.items():
		ada.obs.loc[ada.obs['anno'].isin(l_clus), ['anno']]=cell
	ada.obs.loc[ada.obs['anno'].isin(l_unknown), ['anno']]=missing
	#sort
	l_cat=[i for i in dic_anno.keys() if len(dic_anno[i])>0]
	if len(l_unknown)>0:
		l_cat=l_cat+[missing]
	ada.obs['anno']=pd.Categorical(ada.obs['anno'], categories=l_cat, ordered=True)
	return ada


def plt_anno(ada, f_out, title=None, col='anno', dic_cmap=d_cmap):
	#cmap
	l_cell=ada.obs[col].cat.categories
	cmap=[dic_cmap[i] for i in l_cell]
	#plot
	ax=sc.pl.umap(ada, color=[col], s=60, alpha=1, show=False, legend_loc='right margin', legend_fontsize=10, legend_fontweight='medium', frameon=False, palette=cmap)
	#adjust
	fig = plt.gcf()
	fig.set_size_inches((4.5, 4))
	ax.set_title(title, fontsize=18, pad=10, weight='semibold')
	ax.xaxis.labelpad=10
	ax.yaxis.labelpad=10
	plt.legend(loc=(1.01, 0), frameon=False, prop={'size': 10, 'weight': 'semibold'})
	#save
	plt.tight_layout()
	plt.savefig(f_out, dpi=300)
	plt.close()
	return	


#############################################################################
#anno
ada=anno_ada(ada, d_anno)
ada.write(f'{fd_out}/data.h5ad')

#plot
ada=sc.read(f'{fd_out}/data.h5ad')
f_out=f'{fd_out}/anno.png'
plt_anno(ada, f_out, title='SGN')





