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


def check(dirToScreens):
    import os
    from os import path
    files = []
    for f in os.listdir(dirToScreens):
        if f.endswith(".csv"):
            files.append(f)
    return files

def getDataType(fname):
    if 'ncvoter' in fname:
        return 'ncvoters'
    if 'medpos' in fname:
        return 'medicare'
    if 'INMT4AA1' in fname:
        return 'ncinmates'
    return ''

def calculateMH2Data(pool_size, slicer,lcolumns,permutations,bf_flag,bf_size,bigrams_flag):
    first = True
    rowsize = len(lcolumns)
    # creating pool
    #@UnresolvedImport
    #@UnusedVariable
    pool = multiprocessing.Pool(processes=pool_size, initializer=calcMH.start_process )#@UnusedVariable @UndefinedVariable
    job_args = []
    
    for chunkStart,chunkSize in slicer.chunkify():
        
        slice = [chunkStart,chunkSize]
        
        if (first):
            job_args.append([slicer,slice,True,permutations,rowsize,bf_flag,bf_size,bigrams_flag])            
            first = False
        else:
            job_args.append([slicer,slice,False,permutations,rowsize,bf_flag,bf_size,bigrams_flag])
    
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
        description='Executa a comparacao (calculo de similaridade) de todos os arquivos em um diretorio',
    )
    
    parser.add_argument('dir', action="store", help='Input dir')
    
    parser.add_argument('output_dir', action="store", help='Output dir')
    

    parser.add_argument('-s', action="store",dest="slice",
                        default=1,
                        type=float,
                        help='size of slice in mb')

    parser.add_argument('-e', action="store",dest="encod",
                        default='UTF-8',
                        help='encoding [UTF-8,utf_16_le,...]')
    
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
    
    parser.add_argument('-bigrams', action='store_true',
                    default=False,
                    dest='bigrams_flag',
                    help='Utiliza Bigramas para calcular o minhash')
    
    parser.add_argument('-st', action='store_true',
                    default=False,
                    dest='same_type_flag',
                    help='So compara os que tiverem o mesmo tipo (e.g. ncovter,ncvoters) ')
    
    args = parser.parse_args()
        
    args_dir = args.dir
    args_output_dir = args.output_dir
    permutation = args.permutation
    encrypt = int(args.encrypt)
    slices = args.slice
    encod = args.encod
    process = args.process
    same_type_flag = args.same_type_flag 
    bigrams_flag =  args.bigrams_flag
    
    encrypt_flag = False
    ACTION_1 = 'MH_'
    ACTION_2 = 'SIM_CALC'
    
    if bigrams_flag:
        print("> Inicianodo o calculo de similaridade entre os arquivos com a utilização de bigramas")
    else:
        print("> Iniciando o calculo de similaridade entre os arquivos")
    
    print(">> MH : " + str(permutation))
    
    #encrypt setup
    if encrypt > 0:
        print(">> BF : " + str(encrypt))
        encrypt_flag = True
        ACTION_1 = 'BF_MH_'
        ACTION_2 = 'BF_'+str(encrypt)+'_SIM_CALC'
        
    
    files = check(args_dir)
    
    
    ###
    ### Generating MinHash
    ###
    columns_file = {}
    dt_file = {}
    minhashs    = {}
    
    print("# Calculando MinHash dos dados")
    for f2mh in files:
        print(">>> " + str(f2mh) )
        start_mh = time.time()
        cf = config.getHeaders(getDataType(f2mh))
        #file 1
        file_full_path = args_dir + f2mh
        s1 = Slicer(file_full_path,chunk_size_mb=slices,file_encoding=encod)
        #lista com 1 minhash por atributo
        mhs_1 = calculateMH2Data(process,s1,cf,permutation,encrypt_flag,encrypt,bigrams_flag)
        
        minhashs[f2mh] = mhs_1
        columns_file[f2mh] = cf
        dt_file[f2mh] = getDataType(f2mh)
        
        end_mh = time.time()
        config.writeExecTime2csv(f2mh,ACTION_1+str(permutation)+"_P",start_mh,end_mh)
    
    print("Comparando os Minash")
    done_list = []
    for file1 in files:
        for file2 in files:
            
            if (same_type_flag):
                condition = (dt_file[file1] == dt_file[file2]) 
            else:
                condition = (dt_file[file1] != dt_file[file2])
             
            if file1 != file2:
                
                if condition:                    
                    ok = True
                    
                    for done in done_list:
                        if ( (done[0]==file1 or done[1]==file1) and (done[0]==file2 or done[1]==file2) ):
                            ok = False
                    
                    if ok:
                        start_comp = time.time()
                        #colocando um espaço vazio na primeira coluna dos resultados
                        h2 = columns_file[file2].copy()
                        h2.insert(0,'')
    
                        dados = []
                        dados.append(h2)
    
                        for c1 in columns_file[file1]:
                            linha = []
                            linha.append(c1)
                            for c2 in columns_file[file2]:
                                mhs_1 = minhashs[file1]
                                mhs_2 = minhashs[file2]
                                val = mhs_1[c1].jaccard(mhs_2[c2])
                                linha.append(val)
                                
                            dados.append(linha)
    
                            end_comp = time.time()
                            #adiciona a lista decomparacoesja realizadas
                            done_list.append([file1,file2])
    
                        if encrypt_flag:
                            name = config.writeComparation2csv(args_output_dir,file1,file2,dados,
                                                               encrypt_flag=True,bf_size=encrypt)
                        else:
                            name = config.writeComparation2csv(args_output_dir,file1,file2,dados)
    
                        config.writeExecTime2csv(name,ACTION_2,start_mh,end_mh)
    
    
    print("Done")