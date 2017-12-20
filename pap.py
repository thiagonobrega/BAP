'''
Created on 9 de ago de 2017

@author: Thiago
'''

from analytics.Signatures import SimilaritySignatures
from analytics import Signatures
import pandas as pd
import numpy as np
from util import config
import time

def check(dirToScreens):
    import os
    from os import path
    files = []
    for f in os.listdir(dirToScreens):
        if f.endswith(".pkl"):
            files.append(f)
    return files

def calculateSimilarityMatrix(a,b,theta = 0.8,atheta = 0.05):
    
    mhd = Signatures.generateMinHashSimMatix(a,b)
    ed = Signatures.generateEntropySimMatix(a,b)
    
    #p = (mhd + ed)/2
    p = (mhd * 6)/10+( ed * 4)/10
    tp = p.T.copy()
    
    #a,b,sim_val
    result = []
    
    for col in p.columns:
        coluna = p[col]
        coluna[coluna==0] = None
        media_coluna = coluna.mean()
        
        coluna_selecionada = coluna[coluna >= (1+theta)*media_coluna ]
        if len(coluna_selecionada) > 0:
            chave_linha = coluna_selecionada.idxmax(axis=1)
            linha = tp[chave_linha]
            media_linha = linha.mean()
            linha_selecionada = linha[linha >= (1+theta)*media_linha ]
            if len(linha_selecionada) == 0:
                # a coluna esta correta
                print("0")
                print(col,chave_linha,coluna.max())
                pass
            else:
                if linha_selecionada.idxmax(axis=1) == col:
                    #linha e coluna concordam (match)
                    #print("-")
                    #print(col,chave_linha,coluna.max())
                    r = (chave_linha,col,coluna.max())
                    result.append(r)
                else:
                    n = min(linha_selecionada.max() ,coluna_selecionada.max())
                    m = max(linha_selecionada.max() ,coluna_selecionada.max())
                    dt = 1 - (n/m)
                    if  dt <= atheta:
                        print(dt)
                        # chave linhavem doa
                        # col vem do b
                        r = (chave_linha,col,coluna.max())
                        result.append(r)
                        print(col,chave_linha,coluna.max())
                    pass
    
    return result


def getGoldStandart(name):
    from configparser import ConfigParser
    cparser = ConfigParser()
    cparser.read('confs/gold_standards.ini')
    g = cparser.get(name, 'result').replace('\n','').split('#')
    
    
    gabarito = []
    for op in g:
        v = op.split(',')
        gabarito.append((v[0],v[1]))
    return gabarito

def corrigeResultado(gabarito,results):
    '''
        Retorna o true match,true non match,false match
    '''
    tm = []
    result_nf = []
    for r in results:
        result_nf.append((r[0],r[1]))
        for g in gabarito:
            if (r[0] == g[0]) & (r[1] == g[1]):
                tm.append(g)
    fm = set(result_nf) - set(tm)
    tnm = set(gabarito) - set(tm)
    return tm,tnm,fm
if __name__ == '__main__':
    
    headers = ['gab','file_1','file_2','sample_size','threshold','tm','tnm','fm','precision','recall','f1','detlta','t1','t2']
    
    indir = 'F:\\Mestrado\\Acompanhamento\\SAC18\\experimentos\\exp_round_1\\signatures\\'
    indir = 'C:\\Users\\Thiago\\Desktop\\data\\signatures\\full\\'
    
    dir1 = indir+'trip\\'
    dir2 = indir+'yelp\\'
    files_dir1 = check(dir1)
    files_dir2 = check(dir2)
    
    gab='trip-yelp'
    gabarito = getGoldStandart(gab)
    
#    a = SimilaritySignatures.load(indir + 'trip\\tripadvisor_e_random_selected_10000.pkl')
#    b = SimilaritySignatures.load(indir + 'yelp\\yelp_e_random_selected_10000.pkl')
    
#    result = calculateSimilarityMatrix(a,b,theta=0.8,atheta=0.05)
#    tm, tnm, fm = corrigeResultado(gabarito,result)
    
    saida = []
    
    for file1 in files_dir1:
        for file2 in files_dir2:
            sample_size1 = int(file1.split('_')[-1].split('.')[0])
            filename1 = file1.split('_')[0]+'-'+file1.split('_')[1]
            sample_size2 = int(file2.split('_')[-1].split('.')[0])
            filename2 = file2.split('_')[0]+'-'+file2.split('_')[1]
            
            if sample_size1 == sample_size2:
                a = SimilaritySignatures.load(dir1+file1)
                b = SimilaritySignatures.load(dir2+file2)
                
                for i in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
                    print(5*'-' + str(i) + 5*'-')
                    start = time.time()
                    result = calculateSimilarityMatrix(a,b,theta=i,atheta=0.01)
                    end = time.time()
                    tm, tnm, fm = corrigeResultado(gabarito,result)
                    precision = len(tm)/ (len(tm)+len(fm))
                    recall = len(tm)/ (len(tm)+len(tnm))
                    f1 = 2 * ((precision*recall)/(precision+recall))
                    
                    s = [gab,filename1,filename2,sample_size1,i,len(tm),len(tnm),len(fm),precision,recall,f1,end-start,start,end]
                    saida.append(s)
                    
    config.write('saida-full-trip-yelp.csv',headers,saida)
    
    
    import sys
    sys.exit()
    
    ### VOters
    headers = ['gab','file_1','file_2','sample_size','threshold','tm','tnm','fm','precision','recall','f1','detlta','t1','t2']
    
    #indir = 'F:\\Mestrado\\Acompanhamento\\SAC18\\experimentos\\exp_round_1\\signatures\\'
    
    dir1 = indir+'nc\\'
    dir2 = indir+'ohio\\'
    files_dir1 = check(dir1)
    files_dir2 = check(dir2)
    
    gab='nc-oh'
    gabarito = getGoldStandart(gab)
    
#    a = SimilaritySignatures.load(indir + 'trip\\tripadvisor_e_random_selected_10000.pkl')
#    b = SimilaritySignatures.load(indir + 'yelp\\yelp_e_random_selected_10000.pkl')
    
#    result = calculateSimilarityMatrix(a,b,theta=0.8,atheta=0.05)
#    tm, tnm, fm = corrigeResultado(gabarito,result)
    
    saida = []
    
    for file1 in files_dir1:
        for file2 in files_dir2:
            sample_size1 = int(file1.split('_')[-1].split('.')[0])
            filename1 = file1.split('_')[0]+'-'+file1.split('_')[1]
            sample_size2 = int(file2.split('_')[-1].split('.')[0])
            filename2 = file2.split('_')[0]+'-'+file2.split('_')[1]
            
            if sample_size1 == sample_size2:
                a = SimilaritySignatures.load(dir1+file1)
                b = SimilaritySignatures.load(dir2+file2)
                
                for i in [0.4,0.5,0.6,0.7,0.8,0.9]:
                #for i in [0.5]:
                    print(5*'-' + str(i) + 5*'-')
                    start = time.time()
                    result = calculateSimilarityMatrix(a,b,theta=i,atheta=0.01)
                    end = time.time()
                    tm, tnm, fm = corrigeResultado(gabarito,result)
                    precision = len(tm)/ (len(tm)+len(fm))
                    recall = len(tm)/ (len(tm)+len(tnm))
                    f1 = 2 * ((precision*recall)/(precision+recall))
                    
                    s = [gab,filename1,filename2,sample_size1,i,len(tm),len(tnm),len(fm),precision,recall,f1,end-start,start,end]
                    saida.append(s)
                    
    config.write('saida-ksampler-voters.csv',headers,saida)
    
    import sys
    sys.exit()
    
    a = SimilaritySignatures.load(indir + 'trip\\tripadvisor_e_random_selected_10000.pkl')
    b = SimilaritySignatures.load(indir + 'yelp\\yelp_e_random_selected_10000.pkl')
    
    headers = ['gab','file_1','file_2','sample_size','threshold','tm','tnm','fm','precision','recall','f1','detlta','t1','t2']
    
    gab = 'trip-yelp'
    filename1 = 'trip1'
    filename2 = 'yelp1'
    sample_size1 = '10000'
    
    saida = []
    for i in [0.4,0.5,0.6,0.7,0.8,0.9]:
        print(5*'-' + str(i) + 5*'-')
        start = time.time()
        result = calculateSimilarityMatrix(a,b,theta=i,atheta=0.01)
        end = time.time()
        tm, tnm, fm = corrigeResultado(gabarito,result)
        precision = len(tm)/ (len(tm)+len(fm))
        recall = len(tm)/ (len(tm)+len(tnm))
        f1 = 2 * ((precision*recall)/(precision+recall))
        
        #print(i,len(tm),len(tnm),len(fm))
        s = [gab,filename1,filename2,sample_size1,i,len(tm),len(tnm),len(fm),precision,recall,f1,end-start,start,end]
        saida.append(s)
        
    config.write('saida.csv',headers,saida)
        #print(tm)
        #print(tnm)
        #print(fm)
        
    #print(result)
    #dld = generateDataLengthSimMatix(a,b)
    