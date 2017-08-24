# -*- coding: utf-8 -*-
"""
This class calculates the similarity signature to a dataset. This signatures are :

- Locale Sensitive Hash (LSH) signature
- Data Lengh signature
- Entropy signature

 
Created on Fri Mar 17 09:02:21 2017

@author: Thiago Nobrega
"""

import multiprocessing
from util.slicer import Slicer
import time
import argparse
from analytics.signatures import calcMH
from analytics.signatures import calcEntropy
from analytics.signatures import calcBiGramsLength
from analytics import encryptProcessWraper 
from util import config
from analytics.Signatures import SimilaritySignatures

def calculateBigramsLenght(pool_size,data,lcolumns):
    '''
        Rever para adicionar o intervalor de confianca
    '''
    rowsize = len(lcolumns)
    # creating pool
    pool = multiprocessing.Pool(processes=pool_size, initializer=calcBiGramsLength.start_process )#@UnusedVariable @UndefinedVariable
    job_args = []
    
    for cname in lcolumns:
        job_args.append([data[cname],cname])
    
    pool_outputs = pool.map(calcBiGramsLength.exec_wrap, job_args )
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks
    
    return arrangeEntropy(pool_outputs)

def calculateEntropy(pool_size,data,lcolumns):
    rowsize = len(lcolumns)
    # creating pool
    pool = multiprocessing.Pool(processes=pool_size, initializer=calcEntropy.start_process )#@UnusedVariable @UndefinedVariable
    job_args = []
    
    for cname in lcolumns:
        job_args.append([data[cname],cname])
    
    pool_outputs = pool.map(calcEntropy.exec_wrap, job_args )
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks
    
    return arrangeEntropy(pool_outputs)

def arrangeEntropy(pool_outputs):
    data = {}     
    for x in pool_outputs:
        data[x[0]] = x[1]
    return data

def encryptData(pool_size, slicer,lcolumns,bf_flag,bf_size):
    first = True
    rowsize = len(lcolumns)
    # creating pool
    pool = multiprocessing.Pool(processes=pool_size, initializer=encryptProcessWraper.start_process )#@UnusedVariable @UndefinedVariable
    job_args = []
    
    for chunkStart,chunkSize in slicer.chunkify():
        
        slice = [chunkStart,chunkSize]
        
        if (first):
            job_args.append([slicer,slice,True,rowsize,bf_flag,bf_size])            
            first = False
        else:
            job_args.append([slicer,slice,False,rowsize,bf_flag,bf_size])
    
    pool_outputs = pool.map(encryptProcessWraper.exec_wrap, job_args )
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks
    
    return arrangeEncryptedData(pool_outputs,lcolumns)

def arrangeEncryptedData(pool_outputs,lcolumns):
    data = {}
    
    for i ,column in enumerate(lcolumns):
        data[column] = pool_outputs[0][i]
        
    for output in pool_outputs[1:]:
        for i ,column in enumerate(lcolumns):
            data[column].merge(output[i])
    return data


def calculateMH2Data(pool_size, slicer,lcolumns,permutations,bf_flag,bf_size,bigram_flag):
    first = True
    rowsize = len(lcolumns)
    # creating pool
    pool = multiprocessing.Pool(processes=pool_size, initializer=calcMH.start_process )#@UnusedVariable @UndefinedVariable
    job_args = []
    
    for chunkStart,chunkSize in slicer.chunkify():
        
        slice = [chunkStart,chunkSize]
        
#         print('Slice:' + str(slice[0]) + ',' +str(slice[1]) )
        
        if (first):
            job_args.append([slicer,slice,True,permutations,rowsize,bf_flag,bf_size,bigram_flag])            
            first = False
        else:
            job_args.append([slicer,slice,False,permutations,rowsize,bf_flag,bf_size,bigram_flag])
    
    pool_outputs = pool.map(calcMH.exec_wrap, job_args )
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks
    
    return arrangeMinHash(pool_outputs,lcolumns)

def arrangeMinHash(pool_outputs,lcolumns):
    mhs = {}
    
    for i ,column in enumerate(lcolumns):
        mhs[column] = pool_outputs[0][i]
        
    for output in pool_outputs[1:]:
        for i ,column in enumerate(lcolumns):
            mhs[column].merge(output[i])
    return mhs

def cleanFileName(filename):
    import re
    import os
    return re.split('\.csv',os.path.basename(filename))[0] + ".pkl"
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Arguments to calculate de similarity signatures',
    )
    
    parser.add_argument('file', action="store", help='Input file')

    parser.add_argument('-dt', action="store",dest="data_type",
                        default='ncvoters',
                        help='data format [ncvoters,ncinmates,medicare]')
    
    parser.add_argument('-e', action="store",dest="encod",
                        default='UTF-8',
                        help='encoding [UTF-8,utf_16_le,...]')
    
    parser.add_argument('-s', action="store",dest="slice",
                        default=1,
                        type=float,
                        help='size of slice in mb')
    
    parser.add_argument('-process', action="store", dest='process',
                        default=2,
                        type=int,
                        help='Number of process')
    
    parser.add_argument('-permutation', action='store',
                    default=128,
                    type=int,
                    dest='permutation',
                    help='Number of minhash permutatins (default 128)')
    
    parser.add_argument('-encrypt', action='store',
                    default=0,
                    type=int,
                    dest='encrypt',
                    help='Use BloomFilter to encrypt the data, the lengh of BloomFIlter')
    
    
    args = parser.parse_args()
        
    
    file = args.file
    slices = args.slice
    encod = args.encod
    process = args.process
    data_type = args.data_type
    permutation = args.permutation
    encrypt = int(args.encrypt)
    
    #envarioment vars
    encrypt_flag = False
    bigram_flag = False
    ACTION_1 = 'MH_'
    
    #encrypt setup
    if encrypt > 0:
        encrypt_flag = True
        ACTION_1 = 'BF_MH_'
    
    
    columns_file = config.getHeaders(data_type)
    
    ###
    ### MINHASH GENERATE
    ###
    start_mh = time.time()
    s1 = Slicer(file,chunk_size_mb=slices,file_encoding=encod)
    mhs = calculateMH2Data(process,s1,columns_file,permutation,encrypt_flag,encrypt,bigram_flag)
    end_mh = time.time()
    config.writeExecTime2csv(file,ACTION_1+str(permutation)+"_P",start_mh,end_mh)    
    
    ###
    ### Encrypt
    ### 
    start_enc = time.time()
    s2 = Slicer(file,chunk_size_mb=slices,file_encoding=encod)
    encrypted_data = encryptData(process,s2,columns_file,encrypt_flag,encrypt)
    end_enc = time.time()
    config.writeExecTime2csv(file,"ENCRYPT_"+str(encrypt),start_enc,end_enc)
    
    ###
    ### Entropy calculation
    ###
    start_h = time.time()
    entropy = calculateEntropy(process,encrypted_data,columns_file)
    end_h = time.time()    
    config.writeExecTime2csv(file,"ENTROPY_CALC"+str(encrypt),start_h,end_h)
    
    ###
    ### Entropy calculation
    ###
    start_h = time.time()
    bg_length = calculateBigramsLenght(process,encrypted_data,columns_file)
    end_h = time.time()    
    config.writeExecTime2csv(file,"BIGRAM_CALC"+str(encrypt),start_h,end_h)
    
#     print(entropy)
#     print(bg_length)
    
    sig = SimilaritySignatures(cleanFileName(file),columns_file, 
                               mhs,entropy,bg_length)
    sig.save()
    
    
    
#     print(mhs)    
    print("Done")