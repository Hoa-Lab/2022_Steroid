import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import multiprocessing as mp
from pathlib import Path

#--------------------------------------------------------
n=20

fd_out='./out/b00_de_03_plt-bar'
fd_in='./out/b00_de_02_clean'

#--------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
l_fname=list(Path(fd_in).glob('*.csv'))

#--------------------------------------------------------
def plt_bar(dfi, f_out, title=None, sz=(4.5,8)):
	#have to reset index, since index are duplicated
	dfi=dfi.reset_index()
	dfi.index=dfi.index.astype('str')
	#plot (y has to be index and label later, otherwise there will be error bars)
	sns.set()
	fig, ax=plt.subplots(figsize=sz)
	ax=sns.barplot(x='logfc', y=dfi.index, data=dfi, color='grey', alpha=0.7)
	#adjust
	plt.title(title, fontsize=18, pad=10, weight='semibold')
	ax.set_yticklabels(dfi['gene'])
	plt.xlabel('LogFC', fontsize=18, labelpad=10, weight='semibold')
	plt.ylabel('')
	plt.yticks(fontsize=14, rotation=0, weight='semibold')
	#save
	plt.tight_layout()
	plt.savefig(f_out, dpi=300)
	plt.close()	
	return


def mainf(fname):
	#pp
	name=Path(fname).stem
	s0, s1=name.split('__')
	df=pd.read_csv(fname, index_col=0)
	
	#split df
	df_up=df.iloc[0:n].copy()
	df_down=df.iloc[-n:].copy().iloc[::-1]
	df_down['logfc']=df_down['logfc']*(-1)
	
	#plot
	f_out=f'{fd_out}/{name}_up.png'
	title=f'{s0.replace("_", "-")} vs {s1.replace("_", "-")}\n(Up)'
	plt_bar(df_up, f_out, title=title)
	
	f_out=f'{fd_out}/{name}_down.png'
	title=f'{s0.replace("_", "-")} vs {s1.replace("_", "-")}\n(Down)'
	plt_bar(df_down, f_out, title=title)
	return


############################################################################
with mp.Pool() as p:
	p.map(mainf, l_fname)


