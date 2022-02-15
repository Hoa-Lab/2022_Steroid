import pandas as pd
from pathlib import Path

#------------------------------------------------------------
n=20

prj='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'
fd_out='./out/c00_misc_00_top20'
fd_gene='./out/b00_heatmap_00_pp'
fd_exp=f'{prj}/b00_steroid/out/b00_de_00_pp'
fd_de=f'{prj}/b00_steroid/out/b00_de_02_clean'
f_cnv=f'{prj}/b00_steroid/out/a01_anno_00_clean/conversion.csv'
l_sample=['sys_stero__ctrl', 'tt_stero__ctrl', 'tt_stero__sys_stero']

#-----------------------------------------------------------
Path(fd_out).mkdir(exist_ok=True, parents=True)
df_cnv=pd.read_csv(f_cnv, index_col=0)

####################################################################
for sample in l_sample:
	#load gene
	df_up=pd.read_csv(f'{fd_gene}/{sample}_up.csv', index_col=0)
	df_down=pd.read_csv(f'{fd_gene}/{sample}_down.csv', index_col=0)
	l_up=df_up.index.tolist()[0:n]
	l_down=df_down.index.tolist()[0:n]

	#load
	df_exp=pd.read_csv(f'{fd_exp}/{sample}.csv', index_col=0)	
	df_de=pd.read_csv(f'{fd_de}/{sample}.csv', index_col=0)	
	
	#make df
	df_pos=df_de.loc[df_de['gene'].isin(l_up), :]
	df_pos=df_pos.merge(df_exp, left_index=True, right_index=True)
	df_pos['gene']=pd.Categorical(df_pos['gene'], categories=l_up, ordered=True)
	df_pos=df_pos.sort_values(['gene', 'logfc'], ascending=[True, False])
	df_pos=df_pos.drop_duplicates(subset=['gene'])
	
	df_neg=df_de.loc[df_de['gene'].isin(l_down), :]
	df_neg=df_neg.merge(df_exp, left_index=True, right_index=True)
	df_neg['gene']=pd.Categorical(df_neg['gene'], categories=l_down, ordered=True)
	df_neg=df_neg.sort_values(['gene', 'logfc'], ascending=[True, False])
	df_neg=df_neg.drop_duplicates(subset=['gene'])
	
	#save
	df_pos.to_csv(f'{fd_out}/{sample}_up.csv')	
	df_neg.to_csv(f'{fd_out}/{sample}_down.csv')	
