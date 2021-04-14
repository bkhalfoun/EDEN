

import csv
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
import time




def prepareTrace(trace,countDict,inputDirectory,outputDirectory):
	user=trace.split('.')[0]
	# if user not in countDict:
	# 	idTrace=1
	# 	countDict[user]=idTrace
	# else:
	# 	idTrace=countDict[user]+1
	# countDict[user]=idTrace

	inputFile=os.path.join(inputDirectory, trace)
	df = pd.read_csv(inputFile,names=['ID','lat','lng','timestamp'],encoding ='iso-8859-1')
#	df['timestamp']=pd.to_datetime(df['timestamp'])
#	df['timestamp']=df['timestamp'].apply(lambda x :"%d" % (time.mktime( x.timetuple())*1000+ x.microsecond/1000) )
#	df['user']=user
	del df['ID']
	outputFile=os.path.join(outputDirectory, trace)
	df=df[[ 'lat', 'lng', 'timestamp']]
	df.to_csv(outputFile,index=False,header=False)
	return countDict




directory = sys.argv[1]
outputDirectory = sys.argv[2]



# mkdir the output directory
if not os.path.exists(outputDirectory):
	os.makedirs(outputDirectory)

countDict={}

for filename in os.listdir(directory):
	if filename.endswith(".csv"):
		countDict=prepareTrace(filename, countDict,directory, outputDirectory)

#print(countDict)
