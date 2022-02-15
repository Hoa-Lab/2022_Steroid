prj<-'/mnt/c/Users/gus5/Desktop/a01_proj/a14_steroid'

library(affy)
library(limma)

#------------------------------------------------
fd_out<-'./out/a00_exp_00_load'
fd_in<-paste(prj, 'a00_raw/data/microarray/cel_file/', sep='/')

#-------------------------------------------------
dir.create(fd_out, recursive=TRUE)

####################################################################
data<-ReadAffy()  #need to copy CEL files in the same folder that run this script
eset<-rma(data)
df<-exprs(eset)

write.csv(df,paste(fd_out, 'data.csv', sep='/'))
