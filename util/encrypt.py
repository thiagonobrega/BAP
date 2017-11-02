'''
Created on 9 de abr de 2017

@author: Thiago
'''

import ngram
from lib.mybloom.bloomfilter import BloomFilter


def encryptDataBigram(data,size,fp=0.01,n=2):
    """
        n : 2 = Bigrams
        size : Size of BF
        fp : False positive rate
    """
    bloomfilter = BloomFilter(size,fp)
    index = ngram.NGram(N=n)
    bigrams = list(index.ngrams(index.pad(str(data))))
                    
    for bigram in bigrams:
        bloomfilter.add(str(bigram))
                    
    return bloomfilter

def encryptDataWords(data,size,fp=0.01):
    """
        n : 2 = Bigrams
        size : Size of BF
        fp : False positive rate
    """
    bloomfilter = BloomFilter(size,fp)
    #index = ngram.NGram(N=n)
    #bigrams = list(index.ngrams(index.pad(str(data))))
                    
    for word in data.split():
        bloomfilter.add(str(word))
                    
    return bloomfilter