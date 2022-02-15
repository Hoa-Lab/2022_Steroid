import pandas as pd
from pathlib import Path

#----------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/a00_go_00_gl'
fd_in=f'{prj}/b02_sgn/out/b00_heatmap_00_pp'
l_name=['up', 'down']

#------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)

############################################################
for name in l_name:
	df=pd.read_csv(f'{fd_in}/tt_stero__sys_stero_{name}.csv', index_col=0)
	Path(f'{fd_out}/{name}.txt').write_text('\n'.join(df.index.tolist()))
	
