import pandas as pd
import multiprocessing as mp
from pathlib import Path
import json

#---------------------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/b00_de_00_pp'
f_exp='./out/a00_exp_01_clean/data.csv'
f_param=f'{prj}/a00_raw/meta/param_microarray.json'

l_de=[('tt_stero', 'sys_stero'),
	  ('sys_stero', 'ctrl'),
	  ('tt_stero', 'ctrl')]  

#--------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
df=pd.read_csv(f_exp, index_col=0)

with open(f_param, 'r') as f:
	d_grp=json.load(f)['grp']
	
#---------------------------------------------------------
def mainf(t_de):
	l0, l1=[d_grp[i] for i in t_de]
	
	#get grp0 cols
	l_col0=[]
	for treat in l0:
		l_col0.extend([i for i in df.columns if (treat in i)])
	df0=df.loc[:, l_col0].copy()
	
	#get grp1 col
	l_col1=[]
	for treat in l1:
		l_col1.extend([i for i in df.columns if (treat in i)])
	df1=df.loc[:, l_col1].copy()	
	
	#concat
	df_concat=pd.concat([df0, df1], axis=1)
	
	#design df
	l_design=[t_de[0]]*len(l_col0)+[t_de[1]]*len(l_col1)
	
	#save
	f_out=f'{fd_out}/{t_de[0]}__{t_de[1]}.csv'
	df_concat.to_csv(f_out)
	
	f_out=f'{fd_out}/{t_de[0]}__{t_de[1]}.txt'
	Path(f_out).write_text('\n'.join(l_design))
	return

	
##########################################################################
with mp.Pool() as p:
	p.map(mainf, l_de)

