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

import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats


def start_process():
    multiprocessing.current_process()#@UnusedVariable @UndefinedVariable
    #print('Starting ', multiprocessing.current_process().name)#@UnusedVariable @UndefinedVariable

def exec_wrap(data):
    return run(data[0],data[1])

'''
    Recebe a lista de bf
'''
def run(bf_lists,attribute):
    
    num_bigrams = 0
    len_bf = len(bf_lists)
    
    if not bf_lists:
        return [attribute,0]    
    
    x = pd.DataFrame(pd.np.empty((len_bf,1)) * pd.np.nan)
    for i,bf in enumerate(bf_lists):
        x[0][i] = bf.number_of_elements
        num_bigrams += bf.number_of_elements
    
    bl = float(num_bigrams/len_bf)    
    result = [float(x.mean()),float(x.sem()),len_bf]
    
    return [attribute,result]