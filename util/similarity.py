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
from lib.mybloom.bloomutil import * 

def genEmptySimilarityArrayPerRow(data):
    """
        Gera uma matriz de similaridade vazia,com cabeçalho
    """
    linhas = len(data)
    colunas = len(data[0])
    sa = np.zeros((linhas,colunas))
    
    #set hearder
    for v in range(colunas):
#         sa[0][v] = data[0][v]
        sa[0][v] = -1 
    return sa 

def findSimilar(origina_data,sa,fun,threshold,base_row,weights=[]):
    """
        Retorna o id das colunas simlares
        
        fun = numpy.function (mean,median)
    """
    linhas = len(sa)
    colunas = len(sa[0])
    
    similar = []
    s = ""
    for l in range(1,linhas):
        #correção eliminar a coluna do id
        if fun.__name__ == 'average':
            r = fun(sa[l][1:],weights=weights)
        else:
            r = fun(sa[l][1:])
        if r >= threshold:
#             s = "row["  + str(base_row) + "] similar2 row["  + str(l) + "] : " + str(r)
            if base_row != l:
                if "-dup" not in origina_data[base_row][0]:
                    if  not origina_data[base_row][0] == origina_data[l][0]:
                        s = origina_data[base_row][0] + ";"  + origina_data[l][0] + ";" + str(r)
                        similar.append(s)
    
    return similar

class DecryptFun():
    """ 
    """
    def __init__(self, column , fun_name):
            """
            """
            self.column = int(column)
            self.name = fun_name
            self.paillier_type = ''
            self.paillier_type_param = ''

    def get_column(self):
        return self.column


    def get_name(self):
        return self.name


    def get_paillier_type(self):
        return self.paillier_type


    def get_paillier_type_param(self):
        return self.paillier_type_param


    def set_paillier_type(self, value):
        self.paillier_type = value


    def set_paillier_type_param(self, value):
        self.paillier_type_param = value
    
    def isPaillierAbs(self):
        if self.paillier_type == 'ABS':
            return True
        else:
            return False            

def calculateSimilarityDS(data,base_row_number,decrypt_funs,paillier_pub,paillier_pk):
    linhas = len(data)
    colunas = len(data[0])
    
    output = genEmptySimilarityArrayPerRow(data)
    
    base_row = data[base_row_number]

    for l in range(1,linhas):
        crow = data[l]
        #         
        for fun in decrypt_funs:
            if fun.get_name() == 'E':
                if base_row[fun.get_column()] == crow[fun.get_column()]:
                    output[l][fun.get_column()] = 1
                else:
                    output[l][fun.get_column()] = 0
            elif fun.get_name() == 'B':
                #calcula bloom
                f1 = base_row[fun.get_column()]
                f2 = crow[fun.get_column()]
                s = dice_coefficient(f1,f2)
                output[l][fun.get_column()] = s
            else:
                #paillierdesativado
                param = fun.get_paillier_type_param()
                
                
        
    return output

if __name__ == '__main__':
    import time
    from util.csvutil import *    
    from lib.mybloom.bloomfilter import *
    from util.crypto import *
    from util.data import *
    
    print("Creating keys")
    start_k = time.time()
#     pubkey, prikey = paillier.generate_paillier_keypair(n_length=128)
    end_k = time.time()
    print('Keys created')
    
    
    file = "/media/sf_Mestrado/workspace/python/dptee4RL/data/data-10000-2000-r5.csv"
    file = "/media/sf_Mestrado/workspace/python/dptee4RL/data/mini-data.csv"    
    
    
#     gender = ColumnEncrypter(1, BloomFilter, bigrams=True , size=30, fp=0.01)
#     name = ColumnEncrypter(2, BloomFilter, bigrams=True , size=30, fp=0.01)
    lastname = ColumnEncrypter(3, BloomFilter, bigrams=True , size=30, fp=0.01)
#     birth = ColumnEncrypter(4, BloomFilter, bigrams=True , size=60, fp=0.01)
#     birth = ColumnEncrypter(4, pubkey)
#     salario = ColumnEncrypter(5, BloomFilter, bigrams=True , size=60, fp=0.01)
#     salario = ColumnEncrypter(5, pubkey)
    
#     funs = [gender,name,lastname,birth,salario]
    
    od = convertDateStr2AgeInDays(4,read(file,headers=True))
    
    print("encrypting...")
#     pd = encryptDataSet(od, funs)
    print("encrypted!")
    
    #sim calc
    gender = DecryptFun(1, 'B')
    name = DecryptFun(2, 'B')
    lastname = DecryptFun(3, 'B')
#     birth = DecryptFun(5, 'B')
    birth = DecryptFun(4, 'P')
    birth.set_paillier_type('ABS')
    birth.set_paillier_type_param(365)
#     salario = DecryptFun(6, 'B')
    salario = DecryptFun(5, 'P')
    salario.set_paillier_type('ABS')
    salario.set_paillier_type_param(5000);
    funs = [gender,name,lastname,birth,salario]

    print("rec-1-id;rec-2-id;sim\n")
    saida = ""    
#     for i in range(1,len(pd)):
#         sa = calculateSimilarityDS(pd, i, funs,pubkey, prikey)
#         import numpy as np
#         saida += findSimilar(od,sa, np.mean, 0.8 , i)
#     
    print(saida)