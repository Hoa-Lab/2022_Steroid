import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

#-------------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/b02_violin_01_plt'
f_in='./out/b02_violin_00_pp/data.csv'
f_meta=f'{prj}/a00_raw/meta/cell_p7.json'

l_gene=['Nr3c2', 'Cacna1d', 'Nr3c1']
l_cell=['IHC', 'OHC', 'Deiter', 'Pillar']

#-------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
df=pd.read_csv(f_in, index_col=0)
df['anno']=pd.Categorical(df['anno'], categories=l_cell, ordered=True)

with open(f_meta, 'r') as f:
    d_meta=json.load(f)
cmap=[d_meta[i]['color'] for i in l_cell]

#------------------------------------------------
def plt_violin(df, f_out, title=None, sz=(7,4), cmap='tab20'):
	#plot
	sns.set()
	fig, ax=plt.subplots(figsize=sz)
	ax=sns.violinplot(x='anno', y=gene, data=df, palette=cmap, scale='width')
	#adjust
	ax.set_title(title, weight='semibold', fontsize='22', pad=15)
	plt.xlabel('')
	plt.ylabel('Normalized Counts', fontsize=15, labelpad=15, weight='semibold')
	plt.xticks(fontsize=12, rotation=0, weight='semibold')
	#save
	plt.tight_layout()
	plt.savefig(f_out, dpi=300)
	plt.close()
	return

#################################################################
for gene in l_gene:
    f_out=f'{fd_out}/{gene}.png'
    title=gene
    plt_violin(df, f_out, title=title, cmap=cmap)

