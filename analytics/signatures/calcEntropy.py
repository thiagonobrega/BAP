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
    return run(data[0],data[1])

'''
    Recebe a lista de bf
'''
def run(bf_lists,attribute):
    
    entropy = 0
    len_bf = len(bf_lists)
    
    if not bf_lists:
        return [attribute,0]    
    
    for bf in bf_lists:
        #p_x = float(bf.filter.count(1))/ bf.filter.length()
        p_x = float(bf.filter.count(1))/ ( len_bf * bf.filter.length())
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    
    return [attribute,entropy]