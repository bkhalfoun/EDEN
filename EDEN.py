import sys
import os
import numpy as np
import math
import itertools
import pandas as pd
import datetime as dt
import ntpath
import shutil



inputDirectory=sys.argv[1]
outputDirectory=sys.argv[2]
outputFile=sys.argv[3]

if not os.path.exists(outputDirectory):
	os.makedirs(outputDirectory)


df_result=pd.DataFrame(columns=['Dataset','Lppm','Model','Round', 'Nb_user','Correct', 'Total','Accuracy'] )
configs=[]
configs_name=[]
prediction=[]
target=[]


for i in range(1,15):
	df_nobf=pd.read_csv(inputDirectory+'/NOBF-1800/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)
	df_promesse50=pd.read_csv(inputDirectory+'/distance-50/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)
	df_promesse100=pd.read_csv(inputDirectory+'/distance-100/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)
	df_promesse200=pd.read_csv(inputDirectory+'/distance-200/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)
	df_geoi01=pd.read_csv(inputDirectory+'/epsilon-001/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)
	df_geoi001=pd.read_csv(inputDirectory+'/epsilon-0001/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)
	df_geoi005=pd.read_csv(inputDirectory+'/epsilon-0005/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)
	df_trl1=pd.read_csv(inputDirectory+'/range-1/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)
	df_trl2=pd.read_csv(inputDirectory+'/range-2/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)
	df_trl3=pd.read_csv(inputDirectory+'/range-3/prediction-decentralized-'+str(i)+'.csv',names=['target','prediction','origin-target','STD','AC-precision','AC-recall','AC-fscore'],header=0)

	configs=[df_geoi01,df_geoi001,df_geoi005,df_trl1,df_trl2,df_trl3,df_promesse50,df_promesse100,df_promesse200]
	configs_name=['geoi01','geoi001','geoi005','trl1','trl2','trl3','promesse50','promesse100','promesse200']

	df_pu_day=pd.DataFrame(columns=['IDs','STD','AC-precision','AC-recall', 'AC-fscore','LPPM'] )
	name="NAN"

	listIDs_nobf=df_nobf['origin-target'].tolist()
	listIDs_prom50=df_promesse50['origin-target'].tolist()
	listIDs_prom100=df_promesse100['origin-target'].tolist()
	listIDs_prom200=df_promesse200['origin-target'].tolist()
	ss=set(listIDs_prom50)-set(listIDs_nobf)
	
	if len(ss)!=0:
		for j in list(ss):
			listIDs_prom50.remove(j) 
	ss1=set(listIDs_prom100)-set(listIDs_nobf)
	if len(ss1)!=0:

		for k in list(ss1):
			listIDs_prom100.remove(k) 
	ss2=set(listIDs_prom200)-set(listIDs_nobf)
	if len(ss2)!=0:
		for m in list(ss2):
			listIDs_prom200.remove(m) 

	for index, row in df_nobf.iterrows():
		if row['target'] != row['prediction']:  # naturally protected without any LPPM config
			name='NOBF'
	 		df_pu_day= df_pu_day.append({'IDs': row['origin-target'],'STD':0,'AC-precision':1,'AC-recall':1, 'AC-fscore':1,'LPPM': name}, ignore_index=True)
		else:  # Need to be protected with an LPPM config
			name="NAN"
			maxRecall=-1
			for ind,df in enumerate(configs):  # iterate over all the possible LPPMs
				ligne=df.loc[df['origin-target'] == row['origin-target']]    # get the line of a given config of an LPPM
				if not ligne.empty:
					prediction=ligne['prediction'].tolist()[0]
					target=ligne['target'].tolist()[0]				
					if target!= prediction: # if protected : 
					 	recal=ligne['AC-recall'].tolist()[0]
					 	if recal >= maxRecall:   #testing  according to this variable coverage of the original trace #
					 		maxRecall=recal
					 		name=configs_name[ind]
					 		std=ligne['STD'].tolist()[0]
					 		prec=ligne['AC-precision'].tolist()[0]
					 		fs=ligne['AC-fscore'].tolist()[0]

			if maxRecall!= -1 :
				df_pu_day= df_pu_day.append({'IDs': row['origin-target'],'STD':std,'AC-precision':prec,'AC-recall':maxRecall, 'AC-fscore':fs,'LPPM': name}, ignore_index=True)
			else:
				if row['origin-target'] not in (listIDs_prom50): # it means that this trace was deleted in promesse => protected so we add it
					#print(row['origin-target'])
					df_pu_day= df_pu_day.append({'IDs': row['origin-target'],'STD':str(999999),'AC-precision':str(0),'AC-recall':str(0), 'AC-fscore':str(0),'LPPM': 'promesse50*'}, ignore_index=True)
				elif row['origin-target'] not in  listIDs_prom100:
					df_pu_day= df_pu_day.append({'IDs': row['origin-target'],'STD':str(999999),'AC-precision':str(0),'AC-recall':str(0), 'AC-fscore':str(0),'LPPM': 'promesse100*'}, ignore_index=True)

				elif row['origin-target'] not in  listIDs_prom200:
					df_pu_day= df_pu_day.append({'IDs': row['origin-target'],'STD':str(999999),'AC-precision':str(0),'AC-recall':str(0), 'AC-fscore':str(0),'LPPM': 'promesse200*'}, ignore_index=True)



	total= df_nobf.shape[0]
	correct= total - df_pu_day.shape[0]
	nb_users= len(set(df_nobf['target'].tolist()))
	accuracy=(float(correct) / int(total))
	print(total,correct,nb_users,accuracy)
	df_pu_day.to_csv(outputDirectory+'/protected_users_day'+str(i)+'.csv',index=False)
	df_result=df_result.append({'Dataset':'Privamov','Lppm': 'EDEN','Model': 'AF'+str(i-1),'Round':str(i), 'Nb_user':str(nb_users),'Correct':str(correct),'Total':str(total),'Accuracy': str(accuracy)},ignore_index=True)
df_result.to_csv(outputFile,index=False)
