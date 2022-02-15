from pathlib import Path
import pandas as pd

#--------------------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/a01_anno_00_clean'
f_anno=f'{prj}/a00_raw/data/microarray/annotation/Mouse430_2.na36.annot.csv'
l_col=['Gene Symbol']

#--------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)

############################################################################
#load
df=pd.read_csv(f_anno, index_col=0, comment='#')
df=df.loc[:, l_col]

#clean
df.columns=['Gene']
df=df.loc[df['Gene']!='---', :]
df.to_csv(f'{fd_out}/conversion.csv')
