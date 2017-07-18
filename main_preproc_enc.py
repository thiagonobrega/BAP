# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:11:16 2017

@author: Thiago Nobrega
"""

import multiprocessing
from util.slicer import Slicer
import pandas as pd
import numpy as np
import time
from util import config
import argparse
from util.stats import dataStatsEncrypt
from util.stats import dataProfiler
from util import config
import os
import numpy as np
import scipy as sp
import scipy.stats
from analytics import minhash_util

def checkDir(dirToScreens):
    import os
    from os import path
    files = []
    for f in os.listdir(dirToScreens):
        if f.endswith(".csv"):
            files.append(f)
    return files
    


def mean_confidence_interval(mean,se,n, confidence=0.95):
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)#@UnusedVariable @UndefinedVariable
    return [mean-h,mean,mean+h]

if __name__ == '__main__':
    
#     parser = argparse.ArgumentParser(
#         description='Example with nonoptional arguments',
#     )
#     
#     parser.add_argument('file', action="store", help='Input file')
# 
#     
#     parser.add_argument('-e', action="store",dest="encod",
#                         default='UTF-8',
#                         help='encoding [UTF-8,utf_16_le,...]')
#     
#     parser.add_argument('-s', action="store",dest="slice",
#                         default=1,
#                         type=float,
#                         help='size of slice in mb')
#     
#     parser.add_argument('-process', action="store", dest='process',
#                         default=2,
#                         type=int,
#                         help='Number of process')
#     
#     parser.add_argument('-profile', action='store_true',
#                     default=True,
#                     dest='profile',
#                     help='Turn on debug (data profiling)')
#     
#     parser.add_argument('-encrypt', action='store',
#                     default=0,
#                     type=int,
#                     dest='encrypt',
#                     help='Use BloomFilter to encrypt the data')
#         
#     args = parser.parse_args()
#     
#     
#     
#     file = args.file
#     slices = args.slice
#     encod = args.encod
#     process = args.process
#     encrypt = int(args.encrypt)
#     profile = args.profile
    encrypt_flag = False
    
    profile_file = "data/profile/plano_bigram/"
    
    #dir = 'F:\\temp\\e1\\'
    dir = 'F:\\etapa_01\\data_02\\'
    slices = 4
    encod = 'UTF-8'
    process = 4
    profile = True
    encrypt = 60
    
    if encrypt > 0:
        encrypt_flag = True
    
    
    for lfile in checkDir(dir):
        file = dir + lfile
        print(file)
        data_type = minhash_util.getDataType(lfile)
        columns = config.getHeaders(data_type)
    
        ###
        ### data statistics
        ###
        start_stats = time.time()
        #slicer
        
        s = Slicer(file,chunk_size_mb=slices,file_encoding=encod)
        first = True
        pool_size = process
        
        rowsize = len(columns)
        # creating pool
        pool = multiprocessing.Pool(processes=pool_size, initializer=dataStatsEncrypt.start_process )#@UnusedVariable @UndefinedVariable
        job_args = []
        
        for chunkStart,chunkSize in s.chunkify():
            
            slice = [chunkStart,chunkSize]
            
            #print('Slice:' + str(slice[0]) + ',' +str(slice[1]) )
            
            if (first):
                job_args.append([s,slice,columns,True,rowsize,encrypt])            
                first = False
            else:
                job_args.append([s,slice,columns,False,rowsize,encrypt])
        
        pool_outputs = pool.map(dataStatsEncrypt.exec_wrap, job_args )
        pool.close()  # no more tasks
        pool.join()  # wrap up current tasks
        
        r = pool_outputs[0]
        import sys
        sys.exit()
        
        for rt in pool_outputs[1:]:
            r = np.concatenate((r,rt))
        df = pd.DataFrame(r)
        df.columns = columns
        #definir coluna
        del r
        
        result = {}
        data_length = len(df)
        
        #means = df.mean().tolist()
        means = df.mean().to_dict()
        #standar error of media
        sem = df.sem().to_dict()
        
        for c in columns:
            result[c] = mean_confidence_interval(means[c],sem[c],data_length)
        
        
        end_stats = time.time()
        
    
        config.writeExecTime2csv(file,'DATA_PREPPROC_STATS',start_stats,end_stats)
    
        ##
        ## data profiling
        ##
        ## mean e std_errot of charcater per column
        ##
        if profile:
            start_prof = time.time()
            first = True
            pool_size = process
        
            # creating pool
            pool = multiprocessing.Pool(processes=pool_size, initializer=dataProfiler.start_process )#@UnusedVariable @UndefinedVariable
            job_args = []
    
            s = Slicer(file,chunk_size_mb=slices,file_encoding=encod)
            
            for chunkStart,chunkSize in s.chunkify():
                
                slice = [chunkStart,chunkSize]
                
                #print('Slice:' + str(slice[0]) + ',' +str(slice[1]) )
                
                if (first):
                    job_args.append([s,slice,columns,True,rowsize])            
                    first = False
                else:
                    job_args.append([s,slice,columns,False,rowsize])
            
            pool_outputs = pool.map(dataProfiler.exec_wrap, job_args )
            pool.close()  # no more tasks
            pool.join()  # wrap up current tasks
            
            from collections import Counter
            
            profile = {}
            
            for col in columns:
                profile[col] = {}
            
            for rt in pool_outputs:
                for i,col in enumerate(columns):
                    a = Counter(rt[i])
                    b = Counter(profile[col])
                    profile[col] = dict( a + b )
            
            end_prof = time.time()
    
        #rpath = os.path.split(os.path.abspath(file1))[0] + os.path.sep
        file_name = os.path.split(os.path.abspath(file))[1]
        p_file = "data/profile.csv"
        uniques = []
        
        for c in columns:
            uniques.append(profile[c])
            
        #config.writeDataProfile(p_file,file_name,columns,len(df),uniques)
        
            
        file_name = os.path.split(os.path.abspath(file))[1]
        out = profile_file + file_name
        config.writeDataStats(out,file_name,data_type,columns,result,len(df),profile,encrypt_flag=True)
        
        #writeExecTime2csv(file,'DATA_PREPPROC_STATS',start_stats,end_stats)
        config.writeExecTime2csv(file,'DATA_PREPPROC_PROFILE',start_prof,end_prof)
    
    print("!!!!! Done !!!!!!")
    
    