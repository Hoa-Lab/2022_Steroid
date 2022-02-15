import pandas as pd
from pathlib import Path

#---------------------------------------------------------
fd_out='./out/b01_go_00_gene'
fd_in='./out/b00_de_02_clean'

#---------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
l_fname=list(Path(fd_in).glob('*.csv'))

#######################################################################
for fname in l_fname:
	name=Path(fname).stem
	df=pd.read_csv(fname, index_col=0)
	
	#up
	dfi=df.loc[df['logfc']>1, :].copy()
	dfi=dfi.drop_duplicates(['gene'])
	Path(f'{fd_out}/{name}__up.txt').write_text('\n'.join(dfi['gene'].tolist()))
		
	#down
	dfi=df.loc[df['logfc']<-1, :].copy()
	dfi=dfi.drop_duplicates(['gene'])
	Path(f'{fd_out}/{name}__down.txt').write_text('\n'.join(dfi['gene'].tolist()))	
	
