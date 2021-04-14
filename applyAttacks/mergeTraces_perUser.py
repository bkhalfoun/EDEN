import os
import sys
import glob
import pandas as pd



inputDirectory=sys.argv[1]
outputDirectory=sys.argv[2]

if not os.path.exists(outputDirectory):
	os.makedirs(outputDirectory)

list_ids=[]
for filename in sorted(os.listdir(inputDirectory)):
	if filename.endswith(".csv"):
		ids=filename.split('-')[0]
		list_ids.append(ids)

unique_ids=sorted(list(set(list_ids)))
print(unique_ids)



all_df = pd.DataFrame()
current_id=unique_ids.pop(0)

for filename in sorted(os.listdir(inputDirectory)):
	if filename.split('-')[0]==current_id:
		df=pd.read_csv(inputDirectory+'/'+filename,names=['IDs','lat','lng','timestamp'],header=0)
		all_df=pd.concat([all_df, df])
	else:
		all_df['IDs']=current_id
		all_df.to_csv(outputDirectory+'/'+current_id+'.csv',index=False,header=0)
		current_id=unique_ids.pop(0)
		all_df = pd.DataFrame()

all_df['IDs']=current_id
all_df.to_csv(outputDirectory+'/'+current_id+'.csv',index=False,header=0)
