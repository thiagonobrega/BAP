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

import ngram
from lib.mybloom.bloomfilter import BloomFilter


def encryptData(data,size,fp=0.01,n=2):
    """
        n : 2 = Bigrams
        size : Size of BF
        fp : False positive rate
    """
    bloomfilter = BloomFilter(size,fp)
    index = ngram.NGram(N=n)
    bigrams = list(index.ngrams(index.pad(str(data))))
                    
    for bigram in bigrams:
        bloomfilter.add(str(bigram))
                    
    return bloomfilter

def start_process():
    print('Starting ', multiprocessing.current_process().name)

def exec_wrap(data):
    return run(data[0],data[1],data[2],data[3],data[4],data[5],data[6])

def run(slicer,slice,first,mhperm,rowsize,encrypt_flag,bf_size):
    
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
                    bf = encryptData(str(row[column]),bf_size)
                    local_data = str(bf)
                    pass
                else:
                    local_data = str(row[column])
                
                mh.update(local_data.encode('utf8'))


    #return data_stats
    return mhs
    