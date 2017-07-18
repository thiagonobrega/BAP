# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 17:53:44 2017

@author: Thiago
"""
from util import csvutil
from configparser import ConfigParser
import time
import os
import math

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


def writeDataStats(outfile,filename,data_type,columns,data_stats,bigram_data_stat,data_len,uniques,encrypt_flag=False):
    headers = [ 'filename' , 'length' , 'data_type'  ]
    stats_c = [filename,data_len,data_type]
    
    if encrypt_flag:
        lowerv = "min_num_1_"
        maxv = "max_num_1_"
        uniquesv = "unique_num_1_"
    else:
        lowerv = "lowermean_numchar_column_"
        maxv = "maxmean_numchar_column_"
        uniquesv = "unique_vals_column_"
    
    for c in columns:
        headers.append(lowerv + str(c))
        stats_c.append( math.floor(data_stats[c][0]) )
        headers.append( maxv + str(c))
        stats_c.append( round(data_stats[c][2]) )
        headers.append( uniquesv + str(c))
        stats_c.append( len(uniques[c]) )
        #bigram
        headers.append("min_num_bigram_" + str(c))
#         stats_c.append( math.floor(bigram_data_stat[c][0]) )
        stats_c.append( bigram_data_stat[c][0] )
        headers.append( "max_num_bigram_"+ str(c))
#         stats_c.append( round(bigram_data_stat[c][2]) )
        stats_c.append( bigram_data_stat[c][2] )
        
    
    dados = []
    dados.append(stats_c)
    write(outfile,headers,dados)


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

def writeComparation2csv(output_dir,file1,file2,dados,encrypt_flag=False,bf_size=0):
    rpath = os.path.split(os.path.abspath(file1))[0] + os.path.sep
    
    f1_name = os.path.split(os.path.abspath(file1))[1].split('.csv')[0]
    f2_name = os.path.split(os.path.abspath(file2))[1].split('.csv')[0]
    
    outfile = ''
    
    if (encrypt_flag):
        outfile = output_dir + "BF-" + str(bf_size) + "-result_comp_" + f1_name + "_" + f2_name + ".csv"
    else:
        outfile = output_dir + "result_comp_" + f1_name + "_" + f2_name + ".csv"
    
    write(outfile,[],dados,result=True)
    return f1_name + "_" + f2_name

def writeCompResult2csv(outfile,profile_dict,
                        file1,percent1,file2,percent2,
                        correct,wrong,total,miss,wrong_vals):
    headers = ['file1','data_type_1','percent_1','data_1_length',
               'file2','data_type_2','percent_2','data_2_length',
               'correct','wrong','gabarito','nao_classificados','classificados_errados']
    #rpath = os.path.split(os.path.abspath(file1))[0] + os.path.sep
    dados = []
    
    dados.append(file1)
    from analytics import minhash_util
    dados.append(minhash_util.getDataType(file1))
    dados.append(percent1)
    ofile = file1 + "_random_selected_" + percent1 + ".csv"
    dados.append(profile_dict[ofile])
    
    dados.append(file2)
    dados.append(minhash_util.getDataType(file2))
    dados.append(percent2)
    ofile = file2 + "_random_selected_" + percent2 + ".csv"
    dados.append(profile_dict[ofile])
    
    dados.append(correct)
    dados.append(wrong)
    dados.append(total)
    dados.append(miss)
    dados.append(wrong_vals)
    dados = [dados]
    write(outfile,headers,dados)

