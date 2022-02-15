import pandas as pd
from pathlib import Path
import numpy as np

#---------------------------------------------
fd_out='./out/a00_go_01_clean-go'
fd_in='./out/a00_go_00_gl/go'

#---------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
l_fname=list(Path(fd_in).glob('*.txt'))

#---------------------------------------------
def load_go(fname, n=10):
	#load
	df=pd.read_csv(fname, sep='\t')
	df=df.loc[:, ['Term', 'Combined Score', 'Adjusted P-value', 'Genes']].copy()
	df=df.sort_values(['Combined Score', 'Adjusted P-value'], ascending=False)
	df=df.iloc[0:n, :]
	#clean term
	df['Term']=df['Term'].apply(clean_term)
	return df

def clean_term(term, i=9):
    go=term.split('(GO:')[-1].strip(')')
    #get name
    name=term.split('(GO:')[0].strip()
    if len(l_name:=name.split(' '))>i:
    	name=f'{" ".join(l_name[0:i])}...'
    #concat
    #term=f'(GO:{go}) {name}'	
    term=f'{name}'	
    return term

###############################################################
for fname in l_fname:
    name=Path(fname).stem
    df=load_go(fname)
    df=df.loc[:, ['Term', 'Genes']]
    df.to_csv(f'{fd_out}/{name}.csv', index=False)
    
