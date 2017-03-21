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
import sys

    
if __name__ == '__main__':

    
    exec_name = "bloom"
    time_file = "exec_time_"+exec_name+".csv"
#     tr = open(time_file, "w")
#     tr.write("etapa;sim_fun;threshold;start;end\n")
        
    npp = 32
#     file1 = "F:\\temp\\ncvoter74.txt"
    file1 = "F:\\temp\\ncvoter15.txt"
    file2 = "F:\\temp\\ncvoter76.txt"
#     file2 = "data/data-10000-2000-r5.csv"

    od1 = readQuoted(file1,headers=False)
    od2 = readQuoted(file2,headers=False)
    os1 = sys.getsizeof(od1)
    os2 = sys.getsizeof(od2) 
#     for i in range(0,10):
#         print(od1[i][0],od2[i][0])
#     sys.exit()

    first_name = ColumnEncrypter(10, BloomFilter, bigrams=True , size=60, fp=0.01)
    midl_name = ColumnEncrypter(11, BloomFilter, bigrams=True , size=60, fp=0.01)
    last_name = ColumnEncrypter(9, BloomFilter, bigrams=True , size=60, fp=0.01)
    age = ColumnEncrypter(29, BloomFilter, bigrams=True , size=60, fp=0.01)
    
    funs1 = [first_name,midl_name,last_name,age]
    
    print("encrypting data 1 ...")
    start_c = time.time()
    pd1 = encryptDataSet(od1, funs1)
    end_c = time.time()
    print("encrypted! in", end_c - start_c,"s" )
    
    first_name = ColumnEncrypter(10, BloomFilter, bigrams=True , size=60, fp=0.01)
    midl_name = ColumnEncrypter(11, BloomFilter, bigrams=True , size=60, fp=0.01)
    last_name = ColumnEncrypter(9, BloomFilter, bigrams=True , size=60, fp=0.01)
    age = ColumnEncrypter(29, BloomFilter, bigrams=True , size=60, fp=0.01)
    
    funs1 = [first_name,midl_name,last_name,age]
    
    print("encrypting data 2 ...")
    start_c = time.time()
    pd2 = encryptDataSet(od2, funs1)
    end_c = time.time()
    print("encrypted! in", end_c - start_c,"s")
    
#     tr.write("cifrar os dados;;;"+str(start_c)+";"+str(end_c)+"\n")
    
###
##   DATA 1
# separa as colunas
    c1_name = []
    c1_midlname = []
    c1_lastname = []
    c1_age = []
    
    for i in range(1,len(pd1)):
        c1_name.append(pd1[i][10])
        c1_midlname.append(pd1[i][11])
        c1_lastname.append(pd1[i][9])        
        c1_age.append(pd1[i][29])
    

#     for i in range(0,10):
#         print(pd1[i])
#         print(c1_name[i])
    
#     import sys
#     sys.exit()
###
##   DATA 2
# separa as colunas
    c2_name = []
    c2_midlname = []
    c2_lastname = []
    c2_age = []
    
    for i in range(1,len(pd2)):
        c2_name.append(pd2[i][10])
        c2_midlname.append(pd2[i][11])
        c2_lastname.append(pd2[i][9])        
        c2_age.append(pd2[i][29])
    

    
    
    
    start_min = time.time()
#     print(c_name[1])
#     print(c_dod[1])
###
## DATA 1
    from lib.datasketch import MinHash
    
    
    
    mh_firstname1, mh_midname1 , mh_lastname1 , mh_age1 = MinHash(num_perm=npp), MinHash(num_perm=npp) , MinHash(num_perm=npp), MinHash(num_perm=npp)
    
    for d in c1_name:
        mh_firstname1.update(str(d).encode('utf_8'))
        
    for d in c1_midlname:
        mh_midname1.update(str(d).encode('utf_8'))
    
    for d in c1_lastname:
        mh_lastname1.update(str(d).encode('utf_8'))
        
    for d in c1_age:
        mh_age1.update(str(d).encode('utf_8'))
    
    ###
    end_min = time.time()
    
    print("MinHashed dataset 1!!! in", end_min - start_min,"s")
    start_min = time.time()
## DATA 2
    from lib.datasketch import MinHash
    
    
    mh_firstname2, mh_midname2 , mh_lastname2 , mh_age2 = MinHash(num_perm=npp), MinHash(num_perm=npp) , MinHash(num_perm=npp), MinHash(num_perm=npp)
    
    for d in c2_name:
        mh_firstname2.update(str(d).encode('utf_8'))
        
    for d in c2_midlname:
        mh_midname2.update(str(d).encode('utf_8'))
    
    for d in c2_lastname:
        mh_lastname2.update(str(d).encode('utf_8'))
        
    for d in c2_age:
        mh_age2.update(str(d).encode('utf_8'))
    
    end_min = time.time()
    
    print("MinHashed dataset 2!!! in", end_min - start_min,"s")

    start_j = time.time()
    print("Estimated Jaccard for mh_firstname1 and mh_firstname2 is", mh_firstname1.jaccard(mh_firstname2))
    print("Estimated Jaccard for mh_firstname1 and mh_midname2 is", mh_firstname1.jaccard(mh_midname2))
    print("Estimated Jaccard for mh_firstname1 and mh_lastname2 is", mh_firstname1.jaccard(mh_lastname2))
    print("Estimated Jaccard for mh_firstname1 and mh_age2 is", mh_firstname1.jaccard(mh_age2))
    print(30*"-")
    print("Estimated Jaccard for mh_midname1 and mh_midname2 is", mh_midname1.jaccard(mh_midname2))
    print("Estimated Jaccard for mh_midname1 and mh_lastname2 is", mh_midname1.jaccard(mh_lastname2))
    print("Estimated Jaccard for mh_midname1 and mh_age2 is", mh_midname1.jaccard(mh_age2))
    print(30*"-")
    print("Estimated Jaccard for mh_lastname1 and mh_lastname2 is", mh_lastname1.jaccard(mh_lastname2))
    print("Estimated Jaccard for mh_lastname1 and mh_age2 is", mh_lastname1.jaccard(mh_age2))
    print(30*"-")
    print("Estimated Jaccard for mh_age1 and mh_age2 is", mh_age1.jaccard(mh_age2))
    end_j = time.time()
    
    print("Jaccarded!!! in", end_j - start_j,"s")
    print(20*'#')
    print(20*'#')
    from pympler import asizeof    
    print("Size of Original Dataset 1 : ",os1, "in bytes")
    print("Size of Encrypted Dataset 1 : ",asizeof.asized(pd1), "in bytes")
    print("Size of Original Dataset 2 : ",os2, "in bytes")
    print("Size of Encrypted Dataset 2 : ",asizeof.asized(pd2), "in bytes")
    


    print("Size of minhashs Dataset 1 : 4 x ", asizeof.asized(mh_firstname1) , "in bytes")
    print("Size of minhashs Dataset 1 : 4 x ", asizeof.asized(mh_firstname2) , "in bytes")
    
    
    
    sys.exit()
