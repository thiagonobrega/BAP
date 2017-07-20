'''
Created on 18 de jul de 2017

@author: Thiago Nobrega
@mail: thiagonobrega@gmail.com
'''

import pandas as pd
import numpy as np
import scipy as sp

def generateMinHashSimMatix(a,b):
    '''
        Generate the MinHash similarity matrix
    '''
    
    I = pd.Index(a.columns_names, name="rows")
    C = pd.Index(b.columns_names, name="columns")
    
    #criar
    pdata = pd.DataFrame(pd.np.empty((len(a.columns_names),len(b.columns_names))) * pd.np.nan, index=I, columns=C)
    #column,row
    #pdata['res_state']['mail_zipcode'] = 0
        
    for c_a in a.columns_names:
        for c_b in b.columns_names:
            val = SimilaritySignatures.simMinHash(a,c_a,b,c_b)
            pdata[c_b][c_a] = val
    
    return pdata

def generateEntropySimMatix(a,b):
    '''
        Generate the Entropy similarity matrix
    '''
    
    I = pd.Index(a.columns_names, name="rows")
    C = pd.Index(b.columns_names, name="columns")
    
    #criar
    pdata = pd.DataFrame(pd.np.empty((len(a.columns_names),len(b.columns_names))) * pd.np.nan, index=I, columns=C)
    #column,row
    #pdata['res_state']['mail_zipcode'] = 0
        
    for c_a in a.columns_names:
        for c_b in b.columns_names:
            val = SimilaritySignatures.simEntropy(a,c_a,b,c_b)
            pdata[c_b][c_a] = val
    
    return pdata

def generateDataLengthSimMatix(a,b):
    '''
        Generate the MinHash similarity matrix
    '''
    
    I = pd.Index(a.columns_names, name="rows")
    C = pd.Index(b.columns_names, name="columns")
    
    #criar
    pdata = pd.DataFrame(pd.np.empty((len(a.columns_names),len(b.columns_names))) * pd.np.nan, index=I, columns=C)
    #column,row
    #pdata['res_state']['mail_zipcode'] = 0
        
    for c_a in a.columns_names:
        for c_b in b.columns_names:
            val = SimilaritySignatures.simDataLength(a,c_a,b,c_b)
            pdata[c_b][c_a] = val
    
    return pdata

class SimilaritySignatures(object):
    '''
    classdocs
    '''


    def __init__(self, file_name , colnames, mh,entrop,rawDatalength):
        '''
        Constructor
        '''
        self.file = file_name
        self.columns_names = colnames
        self.minhash = mh
        self.entropy = entrop
        self.__rawDataLength = rawDatalength
        self.setDataLength()
    
    def setDataLength(self,confidence=0.95):
        r = {}
        for key in self.__rawDataLength.keys():
            x = self.__rawDataLength[key]
            r[key] = SimilaritySignatures.__mean_confidence_interval(x[0],x[1], x[2],confidence)
        
        self.data_length = r
        
    @staticmethod    
    def __mean_confidence_interval(mean,se,n,data_confidence):
        import pandas as pd
        import numpy as np
        import scipy as sp
        import scipy.stats
        h = se * sp.stats.t._ppf((1+data_confidence)/2., n-1)#@UnusedVariable @UndefinedVariable
        return [mean-h,mean,mean+h]
    
    
    def save(self,dir="data/signatures/"):
        import pickle
        import os, sys
        try:
            os.mkdir(dir)
        except FileExistsError:
            pass
                
        outfile = dir+str(self.file)
        with open(outfile, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
    
    @classmethod 
    def load(cls,input):
        import pickle
        with open(input, 'rb') as input:
            return pickle.load(input)
    
    
    @classmethod
    def __simEntropy(cls,entropy_u,entropy_w):
        '''
        Calculate the sim entropy
        '''
        e = [ entropy_u, entropy_w]
        sim_entropy = min(e)/max(e)
        return  sim_entropy
    
    @classmethod
    def simEntropy(cls,u,attribute_u,w,attribute_w):
        '''
            Return the entropy Similarity between to attributes
        '''
        return cls.__simEntropy(u.entropy[attribute_u],w.entropy[attribute_w])
    
    ##
    ## data length sim
    ##
    @classmethod
    def __vector_lenght(cls,v):
        '''
        Dimencao do vetor
        '''
        # alterado para utilizar 3 valores (min,mean,max)
        return float(v[2])-float(v[0])
    
    @classmethod
    def __intercetion(cls,u,w):
        '''
         1 - abs | (mean_1 - mean_2) / (mean_1 + mean_2) |
        '''
        # alterado para utilizar 3 valores (min,mean,max)
        u1 = u[0]
        u2 = u[2]
        
        w1 = w[0]
        w2 = w[2]
        
        if (w1 == u1) and (w2 == u2):
            return 1
        
        # sem intercecao
        #menor iqual ou menor 
        #(removido o menor =)
        if (w1 > u2) or (w2 < u1):
            return 0
        
        #resole o problema se comparar com um ponto
        if (u1 == u2) or (w1 == w2):
            if (u1 == 0) or (w1 == 0):
                return 0
            else:
                a = abs(u1-w1)/ (u1 + w1)
                b = abs(u2-w2)/ (u2 + w2)
                return a+b
        
        if (w1 <= u1) and (w2 <= u2):
            return w2-u1
        
        if ( w1 >= u1 ) and (w2 >= u2):
            return u2 - w1
        
        if (w1 >= u1) and (w2 <= u2):
            return w2 - w1
        
        if (w1<= u1) and (w2 >= u2):
            return u2 - u1
    
    @classmethod
    def simDataLength(cls,a,attribute_a,b,attribute_b):
        
        u = a.data_length[attribute_a]
        w = b.data_length[attribute_b]
        
        u_inter_w = cls.__intercetion(u, w)
                
        if u_inter_w == 0:
            sim_dl = 0
        else:
            denominador = (cls.__vector_lenght(u) + cls.__vector_lenght(w))
            if denominador == 0:
                sim_dl = 1 / u_inter_w
            else:
                sim_dl =  (2*u_inter_w)/ denominador
        return sim_dl
    
    @classmethod
    def simMinHash(cls,a,attribute_a,b,attribute_b):
        from lib.mybloom.bloomfilter import BloomFilter
        val = b.minhash[attribute_b].jaccard(a.minhash[attribute_a])
        return val