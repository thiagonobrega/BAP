'''
Created on 15 de mar de 2017

@author: Thiago Nobrega
@mail: thiagonobrega@gmail.com

 thanks to Alistair Martin (http://www.blopig.com/blog/2016/08/processing-large-files-using-python/)
'''

import multiprocessing
import csv
from io import StringIO
from util.slicer import Slicer
import pandas as pd
import numpy as np

def start_process():
    print('Starting', multiprocessing.current_process().name)#@UnusedVariable @UndefinedVariable

def exec_wrap(data):
    return run(data[0],data[1],data[2],data[3],data[4])

def run(slicer,slice,headers,first,rowsize):
    
    sdata = StringIO(slicer.read(slice))
    
    reader = csv.reader(sdata,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL, skipinitialspace=True)
    
    if (first):
        next(reader, None)
    
    dics = []        
    for i in range(0,rowsize):
        dics.append({})
    
    for row in reader:
        row_size = len(row)
        
        try:
            if(rowsize == row_size):                
                for column in range(0,row_size):
                    try:
                        dics[column][str(row[column])] += 1
                    except KeyError:
                        dics[column][str(row[column])] = 1            
            else:
                print('======== erro =======')
                print(row)
        except ValueError:
            print(row)

    #return data_stats
    return dics
    