'''
Created on 12 de abr de 2017

@author: Thiago
'''
from analytics import minhash_util
from math import sqrt

def check(dirToScreens):
    import os
    from os import path
    files = []
    for f in os.listdir(dirToScreens):
        if f.endswith(".csv"):
            files.append(f)
    return files

def classifica(att1,att2,gabarito,rev=False):
    for resp in gabarito:
        resposta = resp
        if (rev):
            resposta = [resp[1],resp[0]]
        
        if (att1 == resposta[0]) and (att2 == resposta[1]):
            return 'TM'
    return 'FM'

def corrigeLinha(att1,dt1,att2,dt2,gabarito):
    if dt1 == 'ncvoters' or dt2 == 'ncvoters':
        if dt1 == 'ncvoters':
            return classifica(h1,h2,gabarito),False
        else:
            return classifica(h1,h2,gabarito,rev=True),True

    if dt1 == 'medicare' or dt2 == 'medicare':
        if dt1 == 'medicare':
            return classifica(h1,h2,gabarito),False
        else:
            return classifica(h1,h2,gabarito,rev=True),True

def buscaTrueNonMatch(file1,data_length1,dt1,file2,data_length2,dt2,espelho_gabartio,gabarito,inv_flag):
    a = set()
    for g in gabarito:
        tupla = tuple(g)
        if inv_flag:
            tupla = (g[1],g[0])
        
        a.add(tupla)
    z = a - espelho_gabarito
    
    r = []
    if len(z) != 0:
        for e in z:
            tnm = [p1['filename'],data_length1,dt1,e[0],p2['filename'],data_length2,dt2,e[1],0,'TNM']
            r.append(tnm)
    
    return r

if __name__ == '__main__':
    profile_dir = 'data/profile/plano_bigram/'
    outfile_prefix =  'data/profile/resumo_'
      
    filenames = check(profile_dir)
    first = True
    dt_set = set()
      
    for fname in filenames:
        dt_set.add(minhash_util.getDataType(fname))
      
    outfiles = {}
    headers = {}
    for element in dt_set:
        file = outfile_prefix + str(element) +'_plano_bigram.csv'
        outfiles[element] =  open(file,'w')
        headers[element] = True
              
    for fname in filenames:
        dt = minhash_util.getDataType(fname)
        outfile = outfiles[dt]
          
        file = profile_dir + fname
        with open(file) as infile:
            header = infile.readline()
            data = infile.readline()
            if headers[dt]:
                headers[dt] = False
                outfile.write(header)
            else:
#                 print(data)
                outfile.write(data)
    
    print("Done profile")
    profile_dir = 'data/profile/'
    filenames = check(profile_dir)
     
    profiles = []
    for fname in filenames:
        file = profile_dir + fname
#        p = minhash_util.readProfile2Dict(file)
        pp = minhash_util.readFullProfile2Dict(file)
        for p in pp:
            profiles.append(p)
     
    from util import config
    
    #####debug
    count_debug = 0
    
    result = []
    result_enchaced = []
    
    for p1 in profiles:
        dt1 = minhash_util.getDataType(p1['filename'])
        hs1 = config.getHeaders(dt1)
        data_length1 = p1['filename'].split('_')[3].split('.')[0]
#         print(p1['filename'])
         
        for p2 in profiles:
            dt2 = minhash_util.getDataType(p2['filename'])
            if dt1 != dt2:
                hs2 = config.getHeaders(dt2)
                data_length2 = p2['filename'].split('_')[3].split('.')[0]
                #gabarito
                gabarito = minhash_util.getGoldStandard(dt1,dt2)
                espelho_gabarito = set()
                
                
                for h1 in hs1[1:]:
                    for h2 in hs2[1:]:
                        u1 = float(p1['min_num_bigram_'+str(h1)])
                        u2 = float(p1['max_num_bigram_'+str(h1)])
#                         unique_vals_column_
                        w1 = float(p2['min_num_bigram_'+str(h2)])
                        w2 = float(p2['max_num_bigram_'+str(h2)])
                        #     min_num_1_
                        #     max_num_1_
                        u = (u1,u2)
                        w = (w1,w2)
                        u_inter_w = minhash_util.intercetion(u, w)
                          
                        d = (minhash_util.vector_lenght(u) + minhash_util.vector_lenght(w))
                        if u_inter_w == 0:
                            sim_dl = 0
                        else:
                            if d == 0:
                                #alterado 1/
                                sim_dl = u_inter_w 
                            else:
                                sim_dl = (2*u_inter_w)/d
                        
                        
                        if ( minhash_util.vector_lenght(u) == 0 ) or (minhash_util.vector_lenght(w) == 0):
                            if (minhash_util.vector_lenght(u) == minhash_util.vector_lenght(w) ):
                                cos_sim = 1
                            else:
                                cos_sim = u_inter_w / sqrt(minhash_util.vector_lenght(u) + minhash_util.vector_lenght(w))
                        else:
                            cos_sim = u_inter_w / sqrt(minhash_util.vector_lenght(u) * minhash_util.vector_lenght(w))
                        
                        classificacao,inv_boolean = corrigeLinha(h1,dt1,h2,dt2, gabarito)
                        if sim_dl > 0:
                            #debug
                            
                            if classificacao == 'TM':
                                espelho_gabarito.add( (h1,h2) )
                            rl = [p1['filename'],data_length1,dt1,h1,p2['filename'],data_length2,dt2,h2,sim_dl,classificacao]
                            result.append(rl)
                            
                            ####debug
                            ######## enhaced
                            max_sim = max([sim_dl,cos_sim])
                            min_sim = min([sim_dl,cos_sim])
                            
                            if (1 - min_sim/max_sim < 0.6):
                                count_debug += 1
                                erl = [p1['filename'],data_length1,dt1,h1,p2['filename'],data_length2,dt2,h2,((sim_dl+cos_sim)/2),classificacao]
                                result_enchaced.append(erl)
#                                 print("-----------")
#                                 print(h1,u)
#                                 print(h2,w)
#                                 print("sim_dl : " , sim_dl)
#                                 print("sim_cos : ", cos_sim)
                            
                    
                    #adiciona o True Non Match
                    tnm_list = buscaTrueNonMatch(p1['filename'],data_length1,dt1, p2['filename'],data_length2,dt2,
                                                 espelho_gabarito, gabarito , inv_boolean)
                
                #  adiciona os tnm ao resultado
                for tnm in tnm_list:
                    result.append(tnm)
                    result_enchaced.append(tnm)
                            
      
    hs = ['file_1','data_length1','data_type_1','attribut_1','file_2','data_length2','data_type_2','attribut_2','sim_dl','classificacao'] 
    ofile = profile_dir + 'analytic.txt'
    config.write(ofile, hs, result)
    
    eofile = profile_dir + 'enchaced-analytic.txt'
    config.write(eofile, hs, result_enchaced)
    print("Done", count_debug)
#     print(result)