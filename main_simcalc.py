# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 09:02:21 2017

@author: Thiago Nobrega
"""

import multiprocessing
from util.slicer import Slicer
import time
import argparse
from asu import calcMH
from util import config



def calculateMH2Data(pool_size, slicer,lcolumns,permutations,bf_flag,bf_size):
    first = True
    rowsize = len(lcolumns)
    # creating pool
    #@UnresolvedImport
    #@UnusedVariable
    pool = multiprocessing.Pool(processes=pool_size, initializer=calcMH.start_process )#@UnusedVariable @UndefinedVariable
    job_args = []
    
    for chunkStart,chunkSize in slicer.chunkify():
        
        slice = [chunkStart,chunkSize]
        
        print('Slice:' + str(slice[0]) + ',' +str(slice[1]) )
        
        if (first):
            job_args.append([slicer,slice,True,permutations,rowsize,bf_flag,bf_size])            
            first = False
        else:
            job_args.append([slicer,slice,False,permutations,rowsize,bf_flag,bf_size])
    
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
            

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Example with nonoptional arguments',
    )
    
    parser.add_argument('file1', action="store", help='Input file')
    
    parser.add_argument('file2', action="store", help='Input file')

    parser.add_argument('-t1', action="store",dest="data_type1",
                        default='ncvoters',
                        help='data format [ncvoters,ncinmates,medicare]')
    
    parser.add_argument('-t2', action="store",dest="data_type2",
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
                    help='Turn on debug (data profiling)')
    
    parser.add_argument('-encrypt', action='store',
                    default=0,
                    type=int,
                    dest='encrypt',
                    help='Use BloomFilter to encrypt the data')
    
    
    args = parser.parse_args()
        
    
    file1 = args.file1
    file2 = args.file2
    slices = args.slice
    encod = args.encod
    process = args.process
    data_type1 = args.data_type1
    data_type2 = args.data_type2
    permutation = args.permutation
    encrypt = int(args.encrypt)
    
    encrypt_flag = False
    ACTION_1 = 'MH_'
    ACTION_2 = 'SIM_CALC'
    
    #encrypt setup
    if encrypt > 0:
        encrypt_flag = True
        ACTION_1 = 'BF_MH_'
        ACTION_2 = 'BF_'+str(encrypt)+'_SIM_CALC'
    
    columns_file1 = config.getHeaders(data_type1)
    columns_file2 = config.getHeaders(data_type2)
    
    ###
    ### MINHASH GENERATE
    ###
    start_mh = time.time()
    #file 1
    s1 = Slicer(file1,chunk_size_mb=slices,file_encoding=encod)
    mhs_1 = calculateMH2Data(process,s1,columns_file1,permutation,encrypt_flag,encrypt)
    
    end_mh = time.time()
    config.writeExecTime2csv(file2,ACTION_1+str(permutation)+"_P",start_mh,end_mh)
    
    # file2
    start_mh = time.time()
    s2 = Slicer(file2,chunk_size_mb=slices,file_encoding=encod)
    mhs_2 = calculateMH2Data(process,s2,columns_file2,permutation,encrypt_flag,encrypt)
    end_mh = time.time()
    config.writeExecTime2csv(file2,ACTION_1+str(permutation)+"_P",start_mh,end_mh)
    
    start_comp = time.time()
    h2 = columns_file2.copy()
    h2.insert(0,'')
    
    dados = []
    dados.append(h2)
    
    for c1 in columns_file1:
        linha = []
        linha.append(c1)
        for c2 in columns_file2:
            val = mhs_1[c1].jaccard(mhs_2[c2])
            linha.append(val)
            
        dados.append(linha)
    
    end_comp = time.time()
    
    #problema aqui 
    #name = config.writeCompResult2csv(file1,file2,dados)
    if encrypt_flag:
        name = config.writeComparation2csv(file1,file2,dados,
                                           encrypt_flag=True,bf_size=encrypt)
    else:
        name = config.writeComparation2csv(file1,file2,dados)
    
    config.writeExecTime2csv(name,ACTION_2,start_mh,end_mh)
    print("Done")