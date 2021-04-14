

import csv
import s2sphere as s2
import sys
import os
import numpy as np
import math
import itertools
import pandas as pd
import functools
import operator
import ntpath
import concurrent.futures
import psutil
import gc




def getLatLng(lat,lng):
	return s2.S2LatLng.FromDegrees(lat,lng)

def getId(lat,lng,level):
	return str(s2.S2CellId(getLatLng(lat,lng)).parent(level).id())

def avgDatetime(series):
 	dt_min = series.min()
 	dt_max = series.max()
 	return dt_min - (dt_max - dt_min)/2.0
.
def divide_chunks(l, n):
	# looping till length l
	for i in range(0, len(l), n):
		yield l[i:i + n]

def manageSubTraceName(traceFile):
	name=traceFile.replace('.csv','')
	idUser=name#.split('_')[0]
	return idUser

def computeHeatMap(trace,level,name):
	with open(trace) as fi:
		ncols = len(fi.readline().split(','))
	if ncols == 3:
		df = pd.read_csv(trace,names=['lat','lng','timestamp'])
	else:
		df = pd.read_csv(trace,names=['user','lat','lng','timestamp'])
		df.pop('user')
	try:
		df['timestamp']=pd.to_datetime(df['timestamp'], unit='ms')
	except:
		df['timestamp']=pd.to_datetime(df['timestamp'])
	ids = df.apply(lambda row: getId(row['lat'], row['lng'],level), axis=1)
	df['IDs'] = ids
	unique= ids.unique()
	#print(str(len(unique)))
	count=df.groupby('IDs')['IDs'].count().to_frame(name=name).reset_index()
	total={'IDs': 'total',name: count[name].sum()}
	count[name]=count[name].apply(lambda x: float(x)/total[name])
	count = count.append(total,ignore_index=True)
	avgdate=avgDatetime(df['timestamp'])
	timeOfHeatMap={'IDs': 'timestamp',name: avgdate}
	count = count.append(timeOfHeatMap,ignore_index=True)
	hourOfHeatMap={'IDs': 'hourOfDay',name: avgdate.hour}
	count = count.append(hourOfHeatMap,ignore_index=True)
	centerLat = df['lat'].mean()
	centerLng = df['lng'].mean()
	centerLatOfHeatMap={'IDs': 'centerLat',name: centerLat}
	count = count.append(centerLatOfHeatMap,ignore_index=True)
	centerLngOfHeatMap={'IDs': 'centerLng',name: centerLng}
	count = count.append(centerLngOfHeatMap,ignore_index=True)
	dic = {}
	for ix in count.index:
		ids=count.loc[ix]['IDs']
		v=count.loc[ix][name]
		if name not in dic:
			dic[name] = {}
		dic[name][ids]=v
	return dic


def computeHeatMapIntoDict(trace,level,name):
	df = pd.read_csv(trace,names=['lat','lng','timestamp'])
	#df['timestamp']=pd.to_datetime(df['timestamp'], unit='ms')
	df['timestamp']=pd.to_datetime(df['timestamp'])
	ids = df.apply(lambda row: getId(row['lat'], row['lng'],level), axis=1)
	df['IDs'] = ids
	unique= ids.unique()
	#print(str(len(unique)))
	count=df.groupby('IDs')['IDs'].count().to_frame(name=name).reset_index()
	total={'IDs': 'total',name: count[name].sum()}
	count[name]=count[name].apply(lambda x: float(x)/total[name])

	count = count.append(total,ignore_index=True)
	timeOfHeatMap={'IDs': 'timestamp',name: avgDatetime(df['timestamp'])}
	count = count.append(timeOfHeatMap,ignore_index=True)
	return count

def processTraceToHeatMap(filename,directory,level):
	trace=os.path.join(directory, filename)
	#print "Process of "+trace
	return computeHeatMap(trace,level,manageSubTraceName(filename))

def mergeOneChunkOfDict(chunk):
	return [ mergedicts(chunk[i],chunk[i+1]) if i+1<len(chunk) else chunk[i] for i in range(0, len(chunk), 2)]

def mergeHeatMapInProcess(l,r):
	return pd.merge(l,r,on='IDs',how="outer")

def dummyProcess(d):
	return d

def writeDataframeProcess(df,name):
	return df.to_csv(name,index=False)


def mergedicts(dict1, dict2):
	d = {}
	for k in set(dict1.keys()).union(dict2.keys()):
		if k in dict1 and k in dict2:
			if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
				d[k]= mergedicts(dict1[k], dict2[k])
			else:
				# If one of the values is not a dict, you can't continue merging it.
				# Value from second dict overrides one in first and we move on.
				d[k]= dict2[k]
				# Alternatively, replace this with exception raiser to alert you of value conflicts
		elif k in dict1:
			d[k]= dict1[k]
		else:
			d[k]=dict2[k]
	return d


directory = sys.argv[1]
level = int(sys.argv[2])
outpath = sys.argv[3]


NB_PROCESS = psutil.cpu_count(logical=False)
CHUNK_SIZE = 128

# Create pool of processes
executor = concurrent.futures.ProcessPoolExecutor(NB_PROCESS)


# For each trace launch the trace processing job
futures = [executor.submit(processTraceToHeatMap,filename,directory,level) for filename in os.listdir(directory) if filename.endswith(".csv") and os.stat(os.path.join(directory,filename)).st_size>0]

# Wait for the processes to finish
concurrent.futures.wait(futures)

#Get result
l = [ f.result() for f in futures]

gc.collect()


# Merge all the Df into one with hiearchical merging
while len(l)!=1:
	# go through dfs two by two and subit a process that merges the two
	# if the last element has no partener just create a dummy process
	# To go through a list two by two use : #indexes= [ (i,i+1) if i+1<len(l) else (i,0) for i in range(0, len(l), 2)]
	nextlevel=[]
	print(str(len(l))+" merges remaining...")
	chunks=divide_chunks(l, CHUNK_SIZE)
	del l
	gc.collect()
	chunkFutures = [executor.submit(mergeOneChunkOfDict,chunk) for index, chunk in enumerate(chunks)]
	concurrent.futures.wait(chunkFutures)
	# get result
	#res = [ cf.result() for cf in chunkFutures]
	# create the new level (flatmap the results)
	l= [ y for x in chunkFutures for y in x.result()]
	gc.collect()


dic= l[0]
HEADERS = {'IDs'}
for k, v in dic.items():
	for k1, v1 in v.items():
		HEADERS.add(k1)
#print(HEADERS)

HEADERS = list(HEADERS)
front= ['centerLng','centerLat','total','timestamp','hourOfDay','IDs']
for h in front:
	HEADERS.insert(0, HEADERS.pop(HEADERS.index(h)))

with open(outpath, "w") as f:
	w = csv.DictWriter( f, HEADERS,restval='0' )
	w.writeheader()
	for key,val in sorted(dic.items()):
		row = {'IDs': key}
		row.update(val)
		w.writerow(row)

