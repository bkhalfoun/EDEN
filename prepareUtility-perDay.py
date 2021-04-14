import sys
import os
import numpy as np
import math
import itertools
import pandas as pd
import datetime as dt
import ntpath
import shutil


#this part of script is to add the std and area coverage metrics to all predictions of each day.

inputDirectory=sys.argv[1]
file_std=sys.argv[2]
file_ac=sys.argv[3]


df_std=pd.read_csv(file_std,names=['IDs','STD'],header=0)
df_ac=pd.read_csv(file_ac,names=['IDs','AC-precision','AC-recall','AC-fscore'],header=0)
df_result=pd.DataFrame(columns=['target','prediction','origin-target','STD', 'AC-precision','AC-recall', 'AC-fscore'] )


for filename in os.listdir(inputDirectory):
	if filename.endswith(".csv"):
		df=pd.read_csv(inputDirectory+'/'+filename,names=['target','prediction','origin-target'],header=0)
		for index, row in df.iterrows():
			df1=df_std.loc[df_std['IDs'] == row['origin-target']]
			if df1.empty:
				std=99999
			else:
				std=df1['STD'].values[0]
			df2=df_ac.loc[df_ac['IDs'] == row['origin-target']]
			prec=df2['AC-precision'].values[0]
			recall=df2['AC-recall'].values[0]
			fscore=df2['AC-fscore'].values[0]
			df_result = df_result.append({'target':row['target'],'prediction':row['prediction'],'origin-target':row['origin-target'],'STD':std,'AC-precision':prec,'AC-recall':recall, 'AC-fscore':fscore }, ignore_index=True)
		print(df_result)
		df_result.to_csv(inputDirectory+'/'+filename,index=False)
		df_result=pd.DataFrame(columns=['target','prediction','origin-target','STD', 'AC-precision','AC-recall', 'AC-fscore'] )




#total= df1.shape[0]





