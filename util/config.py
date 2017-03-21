# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 17:53:44 2017

@author: Thiago
"""
from util import csvutil
from configparser import ConfigParser
import time
import os

def getHeaders(name):
    cparser = ConfigParser()
    cparser.read('confs/data_headers.ini')
    return cparser.get(name, 'columns').replace('\n','').split(',')

def writeExecTime2csv(file,action,start,end):
    stat_file = file.split('.')[0]+"_exec_time.csv"
    stat_file = "data/exec_time.csv"
    header = ['file' , 'action' ,'start_time' , 'end_time' , 'delta' , 'unix_start' , 'unix_end']
    data = [[file,action,time.ctime(start),time.ctime(end),int(end - start), start , end]]
    write(stat_file,header,data)
    
def write(file,headers,data,result=False):
    wmode = 'a'

    if result:
        wmode = 'w'
    else:
        if not os.path.isfile(file):
            data.insert(0,headers)
            wmode = 'w'
    
    csvutil.write(file,data,writemode=wmode)

def writeDataProfile(outfile,file,columns,data_len,uniques):
    
    headers = [ 'file' , 'length' ]
    #for c in columns:
        #headers.append("unique_vals_" + str(c))
    
    dados = []
    dados.append(file)
    dados.append(data_len)
    #for i in uniques:
    #    dados.append(i)

    dados = [dados]
    write(outfile,headers,dados)

def readDataProfile2Dict(file):
    r = {}
    reader = csvutil.read(file,delimiter=";")
    for row in reader:
        r[row[0]] = row[1]
    return r

def writeComparation2csv(file1,file2,dados):
    rpath = os.path.split(os.path.abspath(file1))[0] + os.path.sep
    f1_name = os.path.split(os.path.abspath(file1))[1].split('.csv')[0]
    f2_name = os.path.split(os.path.abspath(file2))[1].split('.csv')[0]
    outfile = rpath + "result_comp_" + f1_name + "_" + f2_name + ".csv"
    print(outfile)
    write(outfile,[],dados,result=True)
    return f1_name + "_" + f2_name

def writeCompResult2csv(outfile,profile_dict,
                        data_type1,percent1,data_type2,percent2,
                        correct,wrong,total):
    headers = ['data_type_1','percent_1','data_1_length',
               'data_type_2','percent_2','data_2_length',
               'correct','wrong','gabarito']
    #rpath = os.path.split(os.path.abspath(file1))[0] + os.path.sep
    dados = []
    
    dados.append(data_type1)
    dados.append(percent1)
    ofile = data_type1 + "_random_selected_" + percent1 + ".csv"
    dados.append(profile_dict[ofile])
    
    dados.append(data_type2)
    dados.append(percent2)
    ofile = data_type2 + "_random_selected_" + percent2 + ".csv"
    dados.append(profile_dict[ofile])
    
    dados.append(correct)
    dados.append(wrong)
    dados.append(total)
    dados = [dados]
    write(outfile,headers,dados)

