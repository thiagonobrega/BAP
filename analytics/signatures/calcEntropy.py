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
import math


def start_process():
    multiprocessing.current_process()#@UnusedVariable @UndefinedVariable
    #print('Starting ', multiprocessing.current_process().name)#@UnusedVariable @UndefinedVariable

def exec_wrap(data):
    return run(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])

'''
    Recebe a lista de bf
'''
#def run(bf_lists,attribute):
def run(slicer,slice,first,mhperm,rowsize,encrypt_flag,bf_size,bf_lists_len):
    
    sdata = StringIO(slicer.read(slice))
    reader = csv.reader(sdata,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL, skipinitialspace=True)
    
    if (first):
        next(reader, None)
        
    entropy_list = []
    for i in range(0,rowsize):
        entropy_list.append(0)
    
    for row in reader:
        row_size = len(row)
        if(rowsize == row_size):
            for column in range(0,row_size):
                if encrypt_flag:
                    #TODO: arrumar filtros de bloom
                    bf = encrypt.encryptData(str(row[column]),bf_size)
                    p_x = float(bf.filter.count(1))/ ( bf_lists_len * bf.filter.length())
                    if p_x > 0:
                        #entropy += - p_x*math.log(p_x, 2)
                        entropy_list[column] += - p_x*math.log(p_x, 2)
        
    
    return entropy_list