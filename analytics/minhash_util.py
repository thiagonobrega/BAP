# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:22:11 2017

@author: Thiago
"""
import csv
from configparser import ConfigParser
from util import config
import math


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

def getDataType(filename):
    if 'INMT4AA1' in filename:
        return 'ncinmates'
    if 'medpos' in filename:
        return 'medicare'
    if 'ncvoter' in filename:
        return 'ncvoters'

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
    return correct,wrong,goldstandard,False

def evaluateB(results,goldstandard):
    correct = []
    wrong = []
    for row_r in results:
        classification = False
        for row_gs in goldstandard:
            if (row_gs[0] == row_r[1]) and (row_gs[1] == row_r[0]):
                classification = True
        # invertendo o gabarito
        #print(row_r[0])
        row_r = (row_r[0],row_r[1])

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
    return correct,wrong,goldstandard,True

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


############## Alteracoes
########## modEval

"""
    Le o profile dos dados e retornar um dicionario 
    dicionario[label] = valor
"""
def readProfile2Dict(prof_file,encoding='UTF-8',
                     delimiter=';',quoting=csv.QUOTE_NONE):
    
    fp = open(prof_file,encoding=encoding)
    reader = csv.reader(fp,delimiter=delimiter,quotechar='"',quoting=quoting, skipinitialspace=True)
    
    lines = []
    
    for r in reader:
        lines.append(r)
    
    odic = {}
    for i in range(len(lines[0])):
        odic[lines[0][i]] = lines[1][i]
    
    return odic

"""
    Le o profile dos dados e retornar um dicionario 
    dicionario[label] = valor
"""
def readFullProfile2Dict(prof_file,encoding='UTF-8',
                     delimiter=';',quoting=csv.QUOTE_NONE):
    
    fp = open(prof_file,encoding=encoding)
    reader = csv.reader(fp,delimiter=delimiter,quotechar='"',quoting=quoting, skipinitialspace=True)
    
    lines = []
    
    for r in reader:
        lines.append(r)
    
    resultados = []
    for linha in range(1,len(lines)):
        odic = {}
        for i in range(len(lines[0])):
            odic[lines[0][i]] = lines[linha][i]
        resultados.append(odic)
    
    return resultados

"""
    Retorna o dois dicionarios com o perfil dos dados
    
    recebe como parametros:
        profile_dir: o diretorio de profile dos dados
        filename: result file name result_file1_file2.csv
    retorna :
        x := dic com as statisticas dos dados 1
        y := dic com as statisticas dos dados 2
    
"""
def getDataProfileInResult(profile_dir,filename):
    fnsplit = filename.split(".csv")[0].split("_")
    f1 =  str(fnsplit[2])+"_"+str(fnsplit[3])+"_"+str(fnsplit[4])+"_"+str(fnsplit[5])+".csv"
    f2 =  str(fnsplit[6])+"_"+str(fnsplit[7])+"_"+str(fnsplit[8])+"_"+str(fnsplit[9])+".csv"
    
    file1 = profile_dir + f1
    file2 = profile_dir + f2
    
    return readProfile2Dict(file1),readProfile2Dict(file2)

# aqui

"""
    Dimencao do vetor
"""
def vector_lenght(v):
    return float(v[1])-float(v[0])

"""
 1 - abs | (mean_1 - mean_2) / (mean_1 + mean_2) |
"""
def intercetion(u,w):
    
    u1 = u[0]
    u2 = u[1]
    
    w1 = w[0]
    w2 = w[1]
    
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

"""
    corrige o com gabarito do mesmo tipo
"""
def evaluateResultsSameType(horizontal_labels,vertical_labels,results):
    
    d1 = getDataModel(horizontal_labels)
    d2 = getDataModel(vertical_labels)
    
    if d1 != d2:
        import sys
        print('os arquivos tem que ser do mesmo tipo')
        sys.exit()
    
    gs = []
    for label in horizontal_labels:
        gs.append([label,label])
    
    return evaluateA(results,gs)



"""
 renomear
 Recalcula a matriz de similaridade
"""
def xpto(h_labels,h_profileData,v_labels,v_profileData,data,w1=0.3,w2=0.7):
    
    col_names_h = config.getHeaders(getDataModel(h_labels)) 
    col_names_v = config.getHeaders(getDataModel(v_labels))
    resultante = []
    sim_entropy_list = []
    
    for i,col_h in enumerate(col_names_h):
        linha_r = []
        linha_e = []
        
        for j,col_v in enumerate(col_names_v):
            u1 = float(h_profileData[ 'lowermean_numchar_column_'+str(col_h)])
            u2 = float(h_profileData[ 'maxmean_numchar_column_'+str(col_h)])
            #m1 = calc_SimilarityDataLength(mi1,mj1)
            
            w1 = float(v_profileData[ 'lowermean_numchar_column_'+str(col_v)])
            w2 = float(v_profileData[ 'maxmean_numchar_column_'+str(col_v)])        
            #m2 = calc_SimilarityDataLength(mi1,mj1)
            
            u = (u1,u2)
            w = (w1,w2)
            
            u_inter_w = intercetion(u, w)
            
            if u_inter_w == 0:
                sim_dl = 0
            else:
                denominador = (vector_lenght(u) + vector_lenght(w))
                if denominador == 0:
                    sim_dl = 1 / u_inter_w
                else:
                    sim_dl =  (2*u_inter_w)/ denominador

            #sim_dl = (m1 + m2)/2
            
            ###
            ### sim entropia
            #unique_vals_column_gender
            #length
            uniques_vals_u = float(h_profileData[ 'unique_vals_column_'+str(col_h)])
            data_length_u = float(h_profileData['length'])
            entropy_u = uniques_vals_u/data_length_u
            
            uniques_vals_w = float(v_profileData[ 'unique_vals_column_'+str(col_v)])
            data_length_w = float(v_profileData['length'])
            entropy_w = uniques_vals_w/data_length_w
            
            
            e = [ entropy_u, entropy_w]
            sim_entropy = min(e)/max(e)
#             print(col_h,col_v)
#             print(e)
            
            ### sim mh
#             sim_mh = data[i][j]
#             r = (sim_dl/2) + (sim_mh/2)
            r = sim_dl
            linha_r.append(r)
            linha_e.append(sim_entropy)
        
        resultante.append(linha_r)
        sim_entropy_list.append(linha_e)
            
    return resultante,sim_entropy_list

def xpto2(h_labels,h_profileData,v_labels,v_profileData,data,threshold_sim_data_length=0.5):
    
    col_names_h = config.getHeaders(getDataModel(h_labels)) 
    col_names_v = config.getHeaders(getDataModel(v_labels))
    resultante = []
    
    for i,col_h in enumerate(col_names_h):
        linha_r = []
        for j,col_v in enumerate(col_names_v):
            u1 = float(h_profileData[ 'lowermean_numchar_column_'+str(col_h)])
            u2 = float(h_profileData[ 'maxmean_numchar_column_'+str(col_h)])
            
            w1 = float(v_profileData[ 'lowermean_numchar_column_'+str(col_v)])
            w2 = float(v_profileData[ 'maxmean_numchar_column_'+str(col_v)])        
            
            
            #unique_vals_column_gender
            u = (u1,u2)
            w = (w1,w2)
            
            u_inter_w = intercetion(u, w)
            
            if u_inter_w == 0:
                sim_dl = 0
            else:
                sim_dl =  (2*u_inter_w)/(vector_lenght(u) + vector_lenght(w))

            sim_mh = data[i][j]
            
            
            if (sim_dl >= threshold_sim_data_length):
                r = 0
            else:
                r = sim_mh
                
            #r = (sim_dl/2) + (sim_mh/2)
            linha_r.append(r)
        
        resultante.append(linha_r)
            
    return resultante
    

def evaluateResultsM(horizontal_labels,vertical_labels,results):
    
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
            
def evaluateMA(results,goldstandard):
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
    return correct,wrong,goldstandard,False


def getResults2(horizontal_labels,vertical_labels,mh_sim,dl_sim,entropy_sim,general_SimilarityThreshold,mh_SimThreshold):
    mr = []
    #TODO REMOVER
    import sys
    
    for i,linha in enumerate(mh_sim):
        mh_line = mh_sim[i]
        dl_line = dl_sim[i]
        entropy_line = entropy_sim[i]
        
        maximo = max(linha)
        m_count = linha.count(maximo)
        
        results_line = []
        results_dic = {}
        
        for element_pos,element in enumerate(mh_line):
            mh_val = mh_line[element_pos]
            dl_val = dl_line[element_pos]
            
            general_sim = (mh_val+dl_val)/2
            
            if general_sim >= general_SimilarityThreshold:
                results_line.append(general_sim)
                try:
                    results_dic[general_sim].append(element_pos)
                except KeyError:
                    results_dic[general_sim] = [ element_pos ]
                

        #segunda passada
        # caso o limite geral não seja satisfeito
        if len(results_line) == 0:
            for element_pos,element in enumerate(mh_line):
                mh_val = mh_line[element_pos]
                if mh_val >= mh_SimThreshold:
                    results_line.append(mh_val)
                    try:
                        results_dic[mh_val].append(element_pos)
                    except KeyError:
                        results_dic[mh_val] = [ element_pos ]
        
        if len(results_line) > 0:
            canditate = max(results_line)
            
            if (results_line.count(canditate) > 1):
                
                canditate_pos = -1
                max_val = -1
                
                # se tiver mais de um resultado desempata pelo maior similaridade de entropia
                for pos in results_dic[canditate]:
                    if entropy_line[pos] > max_val:
                        max_val = entropy_line[pos]
                        canditate_pos = pos
                        match_elements = horizontal_labels[i],vertical_labels[canditate_pos]
                        
            else:
                canditate_pos = results_dic[canditate][0]
                
            
            match_elements = horizontal_labels[i],vertical_labels[canditate_pos]
#             print(match_elements, canditate)
            mr.append(match_elements)
                    
    return mr

# fn = 'BF-60-result_comp_INMT4AA1-a_random_selected_100_medpos-a_random_selected_100.csv'
#fn = 'result_comp_INMT4AA1-a_random_selected_100_medpos-a_random_selected_500'

# x,y = getDataProfileInResult('data/profile/',fn)
