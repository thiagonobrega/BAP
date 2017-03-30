# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:22:11 2017

@author: Thiago
"""
import csv

from configparser import ConfigParser


def getGoldStandard(dt1,dt2):
    name = ''
    if ( (dt1 == 'ncvoters') or (dt2 == 'ncvoters' ) ) and ( (dt1 == 'ncinmates') or (dt2 == 'ncinmates' ) ):
        name = 'ncvoters-ncinmates'
    if ( (dt1 == 'ncvoters') or (dt2 == 'ncvoters' ) ) and ( (dt1 == 'medicare') or (dt2 == 'medicare' ) ):
        name = 'ncvoters-medicare'
    if ( (dt1 == 'ncinmates') or (dt2 == 'ncinmates' ) ) and ( (dt1 == 'medicare') or (dt2 == 'medicare' ) ):
        name = 'medicare-ncinmates'
    
    cparser = ConfigParser()
    cparser.read('confs/gold_standards.ini')
    
    result = []

    g = cparser.get(name, 'result').replace('\n','').split('#')
    
    for op in g:
        result.append(op.split(','))
    
    return result

def getDataModel(labels):
    
    for label in labels:
        if 'npi' in label:
            return 'medicare'
        if 'voter_id' in label:
            return 'ncvoters'
        if 'doc_number' in label:
            return 'ncinmates'
            
    return 'NoNe'
    


def read_minhashCompResult(file,delimiter=';',quoting=csv.QUOTE_NONE,encoding='UTF-8'):
    fp = open(file,encoding=encoding)
    reader = csv.reader(fp,delimiter=delimiter,quotechar='"',quoting=quoting, skipinitialspace=True)
    
    first = True
    header_h = []
    header_v = []
    data = []
    
    for row in reader:
        if first:
            header_v = row[1:]
            first = False
        else:
            header_h.append(row[0])
            content = [float(i) for i in row[1:]] 
            data.append(content)

    fp.close
    return header_h,header_v,data

def getResults(horizontal_labels,vertical_labels,data,percent = 0.5,limiar_l = 0.5):
    mr = []
    
    for i,linha in enumerate(data):
        maximo = max(linha)
        m_count = linha.count(maximo)
        
        if m_count  < len(linha) * percent :
            inv_linha = []
            inv_linha.append(maximo)
            for element in sorted(linha,reverse=True)[1:]:
                if element >= (limiar_l * maximo):            
                    inv_linha.append(element)
            
            for j in inv_linha:
                pos = [k for k,x in enumerate(linha) if x==j]
                for k in pos:
                    a = horizontal_labels[i],vertical_labels[k]
                    mr.append(a)
                    
    return mr

def evaluateA(results,goldstandard):
    correct = []
    wrong = []
    for row_r in results:
        classification = False
        for row_gs in goldstandard:
            if (row_gs[0] == row_r[0]) and (row_gs[1] == row_r[1]):
                classification = True
        if (classification):
            try:
                correct.index(row_r)
            except ValueError:
                correct.append(row_r)
        else:
            try:
                wrong.index(row_r)
            except ValueError:
                wrong.append(row_r)
    return correct,wrong,goldstandard

def evaluateB(results,goldstandard):
    correct = []
    wrong = []
    for row_r in results:
        classification = False
        for row_gs in goldstandard:
            if (row_gs[0] == row_r[1]) and (row_gs[1] == row_r[0]):
                classification = True
        if (classification):
            try:
                correct.index(row_r)
            except ValueError:
                correct.append(row_r)
        else:
            try:
                wrong.index(row_r)
            except ValueError:
                wrong.append(row_r)
    return correct,wrong,goldstandard

def evaluateResults(horizontal_labels,vertical_labels,results):
    
    d1 = getDataModel(horizontal_labels)
    d2 = getDataModel(vertical_labels)
    
    gs = getGoldStandard(d1,d2)
    
    if d1 == 'ncvoters' or d2 == 'ncvoters':
        if d1 == 'ncvoters':
            return evaluateA(results,gs)
        else:
            #d2+'-'+d1
            return evaluateB(results,gs)
    else:
        if d1 == 'medicare' or d2 == 'medicare':
            if d1 == 'medicare':
                return evaluateA(results,gs)
            else:
                return evaluateB(results,gs)

def list_2d_dict(h,v,data):
    r = {}
    for i,l in enumerate(h):
        linha = {}
        for j,c in enumerate(v):
            linha[c] = data[i][j]
        r[l] = linha
    return r