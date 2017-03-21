#!/usr/local/bin/python3
# encoding: utf-8
'''
main -- shortdesc

main is a description

It defines classes_and_methods

@author:     Thiago Nóbrega
@contact:    thiagonobrega@gmail.com
'''
import numpy as np
from util.similarity import *
import time
from util.csvutil import *
from lib.mybloom.bloomfilter import *
from util.data import *
    
if __name__ == '__main__':

    
    exec_name = "bloom"
    time_file = "exec_time_"+exec_name+".csv"
#     tr = open(time_file, "w")
#     tr.write("etapa;sim_fun;threshold;start;end\n")
        
    
    file1 = "data/data-2000-400-r2.csv"
    file2 = "data/data-10000-2000-r5.csv"
    

    name1 = ColumnEncrypter(1, BloomFilter, bigrams=True , size=60, fp=0.01)
    lastname1 = ColumnEncrypter(2, BloomFilter, bigrams=True , size=60, fp=0.01)
    birth1 = ColumnEncrypter(3, BloomFilter, bigrams=True , size=60, fp=0.01)
    death1 = ColumnEncrypter(4, BloomFilter, bigrams=True , size=60, fp=0.01)
    salario1 = ColumnEncrypter(5, BloomFilter, bigrams=True , size=60, fp=0.01)
    funs1 = [name1,lastname1,birth1,death1,salario1]
    
    # DATA 2
    name2 = ColumnEncrypter(2, BloomFilter, bigrams=True , size=60, fp=0.01)
    lastname2 = ColumnEncrypter(3, BloomFilter, bigrams=True , size=60, fp=0.01)
    birth2 = ColumnEncrypter(4, BloomFilter, bigrams=True , size=60, fp=0.01)
    salario2 = ColumnEncrypter(5, BloomFilter, bigrams=True , size=60, fp=0.01)
    funs2 = [name2,lastname2,birth2,salario2]
    
    
    od1 = read(file1,headers=True)
    od2 = read(file2,headers=True)
    
    print("encrypting data 1 ...")
    start_c = time.time()
    pd1 = encryptDataSet(od1, funs1)
    end_c = time.time()
    print("encrypted! in", end_c - start_c,"s" )
    
    print("encrypting data 2 ...")
    start_c = time.time()
    pd2 = encryptDataSet(od2, funs2)
    end_c = time.time()
    print("encrypted! in", end_c - start_c,"s")
#     tr.write("cifrar os dados;;;"+str(start_c)+";"+str(end_c)+"\n")
    
###
##   DATA 1
# separa as colunas
    c1_name = []
    c1_lastname = []
    c1_dob = []
    c1_dod = []
    c1_income = []  
    for i in range(1,len(pd1)):
        c1_name.append(pd1[i][1])
        c1_lastname.append(pd1[i][2])
        c1_dob.append(pd1[i][3])
        c1_dod.append(pd1[i][4])
        c1_income.append(pd1[i][5])
    
###
##   DATA 2
# separa as colunas
    c2_name = []
    c2_lastname = []
    c2_dob = []
    c2_income = []  
    for i in range(1,len(pd2)):
        c2_name.append(pd2[i][2])
        c2_lastname.append(pd2[i][3])
        c2_dob.append(pd2[i][4])
        c2_income.append(pd2[i][5])
    

    
    start_min = time.time()
#     print(c_name[1])
#     print(c_dod[1])
###
## DATA 1
    from lib.datasketch import MinHash
    
    mmh_firstname1, mmh_midname1, mmf_lastname1, mmh_ag1 = MinHash(), MinHash() , MinHash(), MinHash()
    
    for d in c1_name:
        mmh_firstname1.update(str(d).encode('utf_8'))
        
    for d in c1_lastname:
        mmh_midname1.update(str(d).encode('utf_8'))
    
    for d in c1_dob:
        mmf_lastname1.update(str(d).encode('utf_8'))
        
    for d in c1_income:
        mmh_ag1.update(str(d).encode('utf_8'))
    
    ###
## DATA 1
    from lib.datasketch import MinHash
    
    mmh_firstname2, mmh_midname2, mmh_lastname2, mmh_age2= MinHash(), MinHash() , MinHash(), MinHash()
    
    for d in c2_name:
        mmh_firstname2.update(str(d).encode('utf_8'))
        
    for d in c2_lastname:
        mmh_midname2.update(str(d).encode('utf_8'))
    
    for d in c2_dob:
        mmh_lastname2.update(str(d).encode('utf_8'))
        
    for d in c2_income:
        mmh_age2.update(str(d).encode('utf_8'))
    
    end_min = time.time()
    
    print("MinHashed!!! in", end_min - start_min,"s")

    start_j = time.time()
    print("mmh_firstname1 and mmh_firstname2is", mmh_firstname1.jaccard(mmh_firstname2))
    print("mmh_firstname1 and mmh_midname2is", mmh_firstname1.jaccard(mmh_midname2))
    print("mmh_firstname1 and mmh_lastname2is", mmh_firstname1.jaccard(mmh_lastname2))
    print("mmh_firstname1 and mmh_age2is", mmh_firstname1.jaccard(mmh_age2))
    print(30*"-")
    print("mmh_midname1 and mmh_midname2is", mmh_midname1.jaccard(mmh_midname2))
    print("mmh_midname1 and mmh_lastname2is", mmh_midname1.jaccard(mmh_lastname2))
    print("mmh_midname1 and mmh_age2is", mmh_midname1.jaccard(mmh_age2))
    print(30*"-")
    print("mmf_lastname1 and mmh_lastname2is", mmf_lastname1.jaccard(mmh_lastname2))
    print("mmf_lastname1 and mmh_age2is", mmf_lastname1.jaccard(mmh_age2))
    print(30*"-")
    print("mmh_ag1and mmh_age2is", mmh_ag1.jaccard(mmh_age2))
    end_j = time.time()
    
#     print("Jaccarded!!! in", end_j - start_j,"s")
    
    import sys
    sys.exit()
