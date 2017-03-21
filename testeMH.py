'''
Created on 14 de out de 2016

@author:  Thiago Nobrega
@mail: thiagonobrega@gmail.com
'''
from lib.datasketch import MinHash
import sys
import struct
from hashlib import sha1
import numpy as np


data1 = ['joao','jose','maria']
data2 = ['maria','joao','jose']



m1 = MinHash(num_perm=128)
m2 = MinHash(num_perm=128)
for d in data1:
    m1.update(d.encode('utf8'))
for d in data2:
    m2.update(d.encode('utf8'))
    
# 
# print(len(m1.permutations[0]))
# print(len(m2.permutations))
# from pympler import asizeof
# print(asizeof.asized(m1))
# print(asizeof.asized(m2))
# print(pympler.asizeof.asizeof(m2))
# a,b = m1.permutations
# t=u'ola'
# hv = struct.unpack('<I', sha1(t.encode(encoding='utf_8')).digest()[:4])[0]
# _mersenne_prime = (1 << 61) - 1
# _max_hash = (1 << 32) - 1
# temp = a * hv + b
# print(temp)
# print(30*'-')
# phv = np.bitwise_and((a * hv + b) % _mersenne_prime, np.uint64(_max_hash))
# print(phv)
# sys.exit()

from lib.mybloom.bloomfilter import *

bf1,bf2 = BloomFilter(cap=100),BloomFilter(cap=100)

for element in data1:
    bf1.add(element)
    
for element in data2:
    bf2.add(element)

from lib.mybloom.bloomutil import jaccard_coefficient
 
print("Estimated MinHash Jaccard for data1 and data2 is", m1.jaccard(m2))

print("Estimated BloomFilter Jaccard for data1 and data2 is", jaccard_coefficient(bf1, bf2))

s1 = set(data1)
s2 = set(data2)
actual_jaccard = float(len(s1.intersection(s2)))/float(len(s1.union(s2)))
print("Actual Jaccard for data1 and data2 is", actual_jaccard)