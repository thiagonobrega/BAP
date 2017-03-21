'''
Created on 14 de out de 2016

@author:  Thiago Nobrega
@mail: thiagonobrega@gmail.com
'''
from lib.datasketch import MinHash
import ngram

d1 = ['minhash', 'is', 'a', 'probabilistic', 'data', 'structure', 'for',
        'estimating', 'the', 'similarity', 'between', 'datasets']
d2 = ['minhash', 'is', 'a', 'probability', 'data', 'structure', 'for',
        'estimating', 'the', 'similarity', 'between', 'documents']


from lib.mybloom.bloomfilter import BloomFilter


index = ngram.NGram(N=2)
data1 = []
for original_data in d1:
    
    bloomfilter1 = BloomFilter(cap=60)
    bigrams = list(index.ngrams(index.pad(str(original_data))))
                    
    for bigram in bigrams:
        bloomfilter1.add(str(bigram))
    
    data1.append(str(bloomfilter1))
    
data2 = []
for original_data in d2:
    
    bloomfilter1 = BloomFilter(cap=60)
    bigrams = list(index.ngrams(index.pad(str(original_data))))
                    
    for bigram in bigrams:
        bloomfilter1.add(str(bigram))
    
    data2.append(str(bloomfilter1))
    

print(data1)
print(data2)

m1, m2 = MinHash(), MinHash()
for d in data1:
    m1.update(d.encode('utf8'))
for d in data2:
    m2.update(d.encode('utf8'))
print("Estimated Jaccard for data1 and data2 is", m1.jaccard(m2))

s1 = set(data1)
s2 = set(data2)
actual_jaccard = float(len(s1.intersection(s2)))/float(len(s1.union(s2)))
print("Actual Jaccard for data1 and data2 is", actual_jaccard)