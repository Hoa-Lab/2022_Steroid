import pandas as pd
from pathlib import Path

#----------------------------------------------------------
fd_out='./out/b02_lincs_00_gene'
fd_in='./out/b00_de_02_clean'

#----------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
l_fname=list(Path(fd_in).glob('*.csv'))

#######################################################################
for fname in l_fname:
	name=Path(fname).stem
	df=pd.read_csv(fname, index_col=0)
	
	#filter
	df=df.loc[df['pval']<0.05, :]
	df0=df.loc[df['logfc']>1, :].copy()
	df0=df0.drop_duplicates(subset=['gene'])
	df1=df.loc[df['logfc']<-1, :].copy()
	df1=df1.drop_duplicates(subset=['gene'])	
	
	#save
	Path(f'{fd_out}/{name}__up.txt').write_text('\n'.join(df0['gene'].tolist()))
	Path(f'{fd_out}/{name}__down.txt').write_text('\n'.join(df1['gene'].tolist()))
	
	
