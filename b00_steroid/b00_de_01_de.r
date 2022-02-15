#path='/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'

library(limma)
library(affy)

#--------------------------------------------------
fd_out<-'./out/b00_de_01_de'
fd_in<-'./out/b00_de_00_pp'

l_de<-list(c('tt_stero', 'sys_stero'),
	      c('sys_stero', 'ctrl'),
     	  c('tt_stero', 'ctrl')) 

#-------------------------------------------------
dir.create(fd_out)

##################################################################
for (v_de in l_de)
	{
	name<-paste(v_de[1], v_de[2], sep='__')
	
	#load desgin
	f_design<-paste(fd_in, name, sep='/')
	f_design<-paste(f_design, '.txt', sep='')
	design<-scan(f_design, what=character(), sep='\n')
	#the reference level which is the first level of the factor
	design<-model.matrix(~factor(design, levels=c(v_de[2], v_de[1])))
	
	#load exp
	f_in<-paste(fd_in, name, sep='/')
	f_in<-paste(f_in, '.csv', sep='')
	df<-read.csv(f_in, row.names=1)
	
	#limma
	fit<-lmFit(df, design)
	fit<-eBayes(fit)
	res<-topTable(fit, number=Inf)

	#save
	f_out<-paste(fd_out, name, sep='/')
	f_out<-paste(f_out, '.csv', sep='')
	write.csv(res, f_out)
	}
