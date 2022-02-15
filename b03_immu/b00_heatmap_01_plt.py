import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.cluster import AgglomerativeClustering

#-------------------------------------------------------
n_clus=4

prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/b00_heatmap_01_plt'
fd_in='./out/b00_heatmap_00_pp'
f_meta=f'{prj}/a00_raw/meta/cell_immu.json'
l_cell=['Macrophage', 'Monocyte', 'Neutrophil']

d_order={
'sys_stero__ctrl_down': [3,1,2,0],
'sys_stero__ctrl_up': [2,1,3,0],
'tt_stero__ctrl_down': [1,2,0,3],
'tt_stero__ctrl_up': [0,1,3,2],
'tt_stero__sys_stero_down': [0,2,3,1],
'tt_stero__sys_stero_up': [3,0,1,2]
}

#-------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
df_cell=pd.read_csv(f'{fd_in}/cell.csv', index_col=0)

#load fname
l_fname=list(Path(fd_in).glob('*.csv'))
l_fname=[i for i in l_fname if Path(i).stem!='cell']

#load cmap
with open(f_meta, 'r') as f:
	d_meta=json.load(f)
cmap=[d_meta[cell]['color'] for cell in l_cell]

#-------------------------------------------------------
def plt_top(df, f_out, cmap=None):
	#plot
	fig, ax=plt.subplots(figsize=(12, 4))
	ax=sns.heatmap(df, cmap=cmap, cbar=False)
	#adjust
	ax.xaxis.label.set_visible(False)
	ax.yaxis.label.set_visible(False)
	plt.xticks([])
	plt.yticks([])
	#save
	plt.savefig(f_out, dpi=300)
	plt.close()	
	return


def plt_hm(df, f_out, sz=(8,14), cbar=False):
	#plot
	fig, ax=plt.subplots(figsize=sz)
	ax=sns.heatmap(df, cmap='Purples', vmin=-0.1, cbar=cbar)
	#adjust
	ax.xaxis.label.set_visible(False)
	ax.yaxis.label.set_visible(False)
	plt.yticks(fontsize=9, rotation=0, weight='semibold')
	plt.xticks([])
	#save
	plt.savefig(f_out, dpi=300)
	plt.close()	
	return
	

def mainf(fname, n_clus=n_clus):
	name=Path(fname).stem
	df=pd.read_csv(fname, index_col=0)
	#scale
	df=df.div(df.max(axis=1), axis=0)
	#cluster exp (optional)
	cluster=AgglomerativeClustering(n_clusters=n_clus, affinity='euclidean', linkage='ward')
	cluster.fit_predict(df.values)
	df['_clus']=cluster.labels_
	#sort by cluster (optional)
	l_order=d_order[name]
	df['_clus']=pd.Categorical(df['_clus'], categories=l_order, ordered=True)
	df=df.sort_values('_clus')
	df=df.drop('_clus', axis=1)
	#plot
	f_out=f'{fd_out}/{name}.png'
	plt_hm(df, f_out)
	return
	

##########################################################################
#plot top
df_cell['anno']=df_cell['anno'].replace(l_cell, list(range(len(l_cell))))
df_cell=df_cell.T

f_out=f'{fd_out}/top.png'
plt_top(df_cell, f_out, cmap=cmap)

#plot heatmap
for fname in l_fname:
	mainf(fname)



