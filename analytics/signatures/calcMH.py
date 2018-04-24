'''
Created on Fri Mar 17 09:02:21 2017

@author: Thiago Nobrega
@mail: thiagonobrega@gmail.com

'''

import multiprocessing
import csv
from io import StringIO
from util.slicer import Slicer
from lib.datasketch import MinHash
from util import encrypt
import ngram
from lib.mybloom.bloomfilter import BloomFilter


def start_process():
    multiprocessing.current_process()#@UnusedVariable @UndefinedVariable
    #print('Starting ', multiprocessing.current_process().name)#@UnusedVariable @UndefinedVariable

def exec_wrap(data):
    return run(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])

def run(slicer,slice,first,mhperm,rowsize,encrypt_flag,bf_size,bigrams_flag):
    
    mhs = [] 
    
    for i in range(0,rowsize):
        mh = MinHash(num_perm=mhperm)
        mhs.append(mh)
        
    sdata = StringIO(slicer.read(slice))
    
    reader = csv.reader(sdata,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL, skipinitialspace=True)
    #reader = csv.reader(sdata,delimiter=',',quotechar='"',quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
    
    if (first):
        next(reader, None)
    
    dics = []        
    for i in range(0,rowsize):
        dics.append({})
    
    for row in reader:
        row_size = len(row)
        if(rowsize == row_size):
            for column in range(0,row_size):
                mh = mhs[column]
                local_data = ''
                if encrypt_flag:
                    #TODO: arrumar filtros de bloom
                    if bigrams_flag:
                        bf = encrypt.encryptDataBigram(str(row[column]),bf_size)
                    else:
                        bf = encrypt.encryptDataWords(str(row[column]),bf_size)
                    local_data = str(bf)
                    pass
                else:
                    #rever isso possivel problem (nao utilizado)
                    import ngram
                    index = ngram.NGram(N=2)
                    bigrams_list = list(index.ngrams(index.pad(str(row[column]))))
                    local_data = str(row[column])                    
                
                    if bigrams_flag:
                        for bigram in bigrams_list:
                            mh.update(bigram.encode('utf8'))
                
                mh.update(local_data.encode('utf8'))


    #return data_stats
    return mhs

def run_1(slicer,slice,first,mhperm,rowsize,encrypt_flag,bf_size):
    
    mhs = [] 
    
    for i in range(0,rowsize):
        mh = MinHash(num_perm=mhperm)
        mhs.append(mh)
        
    sdata = StringIO(slicer.read(slice))
    
    reader = csv.reader(sdata,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL, skipinitialspace=True)
    
    if (first):
        next(reader, None)
    
    dics = []        
    for i in range(0,rowsize):
        dics.append({})
    
    for row in reader:
        row_size = len(row)
        if(rowsize == row_size):
            for column in range(0,row_size):
                mh = mhs[column]
                local_data = ''
                if encrypt_flag:
                    bf = encrypt.encryptDataBigram(str(row[column]),bf_size)
                    local_data = str(bf)
                    pass
                else:
                    local_data = str(row[column])
                
                mh.update(local_data.encode('utf8'))


    #return data_stats
    return mhs
    