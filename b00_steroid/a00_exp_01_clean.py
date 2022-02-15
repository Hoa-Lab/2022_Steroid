from pathlib import Path
import pandas as pd

#--------------------------------------------------------
prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/a00_exp_01_clean'
f_in='./out/a00_exp_00_load/data.csv' 
f_info=f'{prj}/a00_raw/data/microarray/aInfo.csv'

#--------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
df=pd.read_csv(f_in, index_col=0)
df_info=pd.read_csv(f_info)

#######################################################################
#remove space in file names
df.columns=[i.replace(' ', '') for i in df.columns]

#clean info
df_info=df_info.sort_values('od')
df_info['Sample ID']=df_info['Sample ID'].apply(lambda x: x.replace(' ', ''))
df_info['Treatment']=df_info['Treatment'].apply(lambda x: x.replace(' ', '_'))
df_info['Treatment']=df_info['Treatment']+'__'+df_info['od'].astype('str')

#replace col name
df_info=df_info.set_index('Sample ID')
df_info=df_info.reindex(df.columns)
df.columns=df_info['Treatment'].tolist()

#sort columns
df=df.T.sort_index().T
df.to_csv(f'{fd_out}/data.csv')

#export probe file for conversion
Path(f'{fd_out}/probe.txt').write_text('\n'.join(df.index.tolist()))
