# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 16:01:08 2017

@author: Thiago
"""
from analytics import minhash_util
from util import config

def check(dirToScreens):
    import os
    from os import path
    files = []
    for f in os.listdir(dirToScreens):
        if f.endswith(".csv"):
            files.append(f)
    return files

def getIndexOf(word,predicate,wordlist):
    for ww in wordlist:
        if predicate in ww:
            if word in ww:
                return wordlist.index(ww)

#monta os resultados para plotar o grafico com percentual de similaridade vs valores unicos
def montaResultados2(resultado,mh_sim,dl_sim,hl_data,vl_data,data_file1,data_file2,status,generalThreshold,mhThreshold):
    linhas = []
    for res in resultado:
        file_1 = data_file1[1][0]
        data_model1 = minhash_util.getDataModel(hl_data)        
        nlf1 = file_1.split('_')[3].split('.')[0]
        label_h = res[0]

        file_2 = data_file2[1][0]
        data_model2 = minhash_util.getDataModel(vl_data)
        nlf2 = file_2.split('_')[3].split('.')[0]
        label_v = res[1]

        #nao esquecer do status
        mh_sim_val = mh_sim[hl_data.index(label_h)][vl_data.index(label_v)]
        dl_sim_val = dl_sim[hl_data.index(label_h)][vl_data.index(label_v)]
        general_sim_val = (mh_sim_val + dl_sim_val)/2
        
        if (general_sim_val < generalThreshold):
            sim_val = mh_sim_val
        else:
            sim_val = general_sim_val
        
        linha = [file_1,data_model1,nlf1,label_h,
                 file_2,data_model2,nlf2,label_v,
                 status,general_sim_val,mh_sim_val,dl_sim_val,sim_val]
        
        linhas.append(linha)
    return linhas
        

if __name__ == '__main__':
    di = 'F:\\results\\data02_01042017\\same_type\\bigrams\\MH256\\'
    data_dir = 'data/'
    output = 'sametype.csv'

    
    
    outfile = data_dir + output
    r2_outfile = data_dir + 'r2-' + output
    
    
#     headers_r2 = ['file_1','data_model_file1','normalized_length_file1','length_file_1','attribute_1','unique_attribute_1','mean_min_atribute_1','mean_max_atribute_1',
#                    'file_2','data_model_file2','normalized_length_file2','length_file_2','attribute_2','unique_attribute_2','mean_min_atribute_2','mean_max_atribute_2',
#                    'status','sim_val']    
#
    headers_r2 = ['file_1','data_model_file1','normalized_length_file1','attribute_1',
                  'file_2','data_model_file2','normalized_length_file2','attribute_2',
                  'status','general_sim_val','mh_sim_val','dl_sim_val','sim_val']
    r2 = []
    
    
    missed = {}
    most_wrong = {}

    data_profile_dir = 'data/profile/plano_bigram/'
    
    files = check(di)

    for file in files:
        print("### " + file)
        
        h,v,sim_mh = minhash_util.read_minhashCompResult(di + file)
        
        # incluido o similaridade do comprimento do atriburo
        h_profileData,v_profileData = minhash_util.getDataProfileInResult(data_profile_dir,file)
        
        sim_dl,entropy_sim = minhash_util.xpto(h,h_profileData,v,v_profileData,sim_mh)
        
        #results = minhash_util.getResults(h,v,d,limiar_l=0.5)
        l1 = 0.5
        l2 = 0.7
        results = minhash_util.getResults2(h,v,sim_mh,sim_dl,entropy_sim,l1,l2)
        
        correct, wrong ,gabarito , gs_inverted_flag = minhash_util.evaluateResultsSameType(h,v,results)
        
        
        ##gerar estatisticas de erros
        #convertendo gabarito
        temp = []
        for i in gabarito:
            if (gs_inverted_flag):
                temp.append(tuple([i[1],i[0]]))
            else:
                temp.append(tuple(i))
        gabarito = temp
        
        #miss = set(gabarito) - set(correct)
        
        miss = set()
        
#         for ga in (set(gabarito) - set(correct)):
#             for answer in correct:
#                     if ( answer[0] == ga[1] and answer[1] == ga[0]):
#                         pass
#                     else:
#                         if (gs_inverted_flag):
#                             miss.add((ga[1],ga[0]))
#                         else:
#                             miss.add(ga)
#         miss =  list(miss)
        miss = list(set(gabarito) - set(correct))
        
        
        # debug
#         print("gabarito : ",gabarito)
#         print("correto : ",correct)
#         print("errado : ",wrong)
#         print("miss : ",miss)
        
            
        for j in miss:
            try:
                missed[j] += 1
            except KeyError:
                missed[j] = 1
        
        for j in wrong:
            try:
                most_wrong[j] += 1
            except KeyError:
                most_wrong[j] = 1
        
        line = file.split('_')
        dt1 = line[2]
        p1 = line[5]
        dt2 = line[6]
        p2 = line[9].split('.csv')[0]
        
        prof_d = config.readDataProfile2Dict('data\profile.csv')
#         config.writeCompResult2csv(outfile,prof_d,dt1,p1,dt2,p2,
#                                    len(correct),len(wrong),
#                                    len(gabarito),list(miss),wrong)
#         
        sfn = file.split('_')
        
        fn1 = sfn[2] +'_'+ sfn[3] +'_'+ sfn[4] +'_'+ sfn[5] + '.csv'
        fn2 = sfn[6] +'_'+ sfn[7] +'_'+ sfn[8] +'_'+ sfn[9]
        
        from util import csvutil
        rows_f1 = csvutil.read(data_profile_dir+fn1,delimiter=";",headers=True)
        rows_f2 = csvutil.read(data_profile_dir+fn2,delimiter=";",headers=True)
        
        
        try:
            r_tm = montaResultados2(correct,sim_mh,sim_dl,h,v,rows_f1,rows_f2,'TM',l1,l2)
            r_tnm = montaResultados2(miss,sim_mh,sim_dl,h,v,rows_f1,rows_f2,'TNM',l1,l2)
            r_fm = montaResultados2(wrong,sim_mh,sim_dl,h,v,rows_f1,rows_f2,'FM',l1,l2)
        except:
            print(gabarito)
            print(correct)
            print(miss)
            
            import sys
            sys.exit()
            
        
        
        
        rf = r_fm+r_tnm+r_tm
        r2 = r2 + rf
    
    r2 = [headers_r2] + r2
    config.write(r2_outfile,headers_r2,r2,result=True)
            
            
    
    print("=========== MISSED ===========")
    print(missed)
    print("=========== MOST WRONG ===========")
    print(most_wrong)
    print('Done!')