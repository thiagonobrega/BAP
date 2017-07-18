'''
Created on 18 de mar de 2017

@author: Thiago
'''
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
def montaResultados2(resultado,sim_data,hl_data,vl_data,data_file1,data_file2,status):
    linhas = []
    for res in resultado:
        file_1 = data_file1[1][0]
        data_model1 = minhash_util.getDataModel(hl_data)        
        nlf1 = file_1.split('_')[3].split('.')[0]
        length_file_1 = data_file1[1][1]
        label_h = res[0]
        uniques_a1 = data_file1[1][getIndexOf(label_h,'unique',data_file1[0])]
        mean_min_a1 = data_file1[1][getIndexOf(label_h,'lowermean',data_file1[0])]
        mean_max_a1 = data_file1[1][getIndexOf(label_h,'maxmean',data_file1[0])]
            
        file_2 = data_file2[1][0]
        data_model2 = minhash_util.getDataModel(vl_data)
        nlf2 = file_2.split('_')[3].split('.')[0]
        length_file_2 = data_file2[1][1]
        label_v = res[1]
        uniques_a2 = data_file2[1][getIndexOf(label_v,'unique',data_file2[0])]
        mean_min_a2 = data_file2[1][getIndexOf(label_v,'lowermean',data_file2[0])]
        mean_max_a2 = data_file2[1][getIndexOf(label_v,'maxmean',data_file2[0])]
        #nao esquecer do status    
        sim_val = sim_data[hl_data.index(label_h)][vl_data.index(label_v)]
        linha = [file_1,data_model1,nlf1,length_file_1,label_h,uniques_a1,
                 mean_min_a1,mean_max_a1,
                 file_2,data_model2,nlf2,length_file_2,label_v,uniques_a2,
                 mean_min_a2,mean_max_a2,
                 status,sim_val]
        
        linhas.append(linha)
    return linhas
        

if __name__ == '__main__':
    #file = 'C:\\Users\\Thiago\\Desktop\\result_comp_ncvoter_random_selected_0_medpos_random_selected_0.csv'
    
    #h,v,d = minhash_util.read_minhashCompResult(file)
    #results = minhash_util.getResults(h,v,d,limiar_l=0.9)
    #correct, wrong = minhash_util.evaluateResults(h,v,results)
    #data = minhash_util.list_2d_dict(h,v,d)
    #f = 'result_comp_medpos_random_selected_0.075p_INMT4AA1_random_selected_0.0025p.csv'
    di = 'F:\\results\\data02_01042017\\bf\\'
    #di = 'F:\\temp\\debug\\'
    #di = 'F:\\results\\18032017\\'
    #di = 'F:\\results\\debug\\'
    data_dir = 'data/'
    output = 'bf01042017.csv'
    #outfile = 'data/22032017.csv'
    
    
    outfile = data_dir + output
    r2_outfile = data_dir + 'r2-' + output
    
    
    headers_r2 = ['file_1','data_model_file1','normalized_length_file1','length_file_1','attribute_1','unique_attribute_1','mean_min_atribute_1','mean_max_atribute_1',
                   'file_2','data_model_file2','normalized_length_file2','length_file_2','attribute_2','unique_attribute_2','mean_min_atribute_2','mean_max_atribute_2',
                   'status','sim_val']    
    r2 = []
    
    
    missed = {}
    most_wrong = {}
    
    files = check(di)
    for file in files:
        h,v,d = minhash_util.read_minhashCompResult(di + file)
        results = minhash_util.getResults(h,v,d,limiar_l=0.5)
        
        correct, wrong ,gabarito , gs_inverted_flag = minhash_util.evaluateResults(h,v,results)
        
        ##gerar estatisticas de erros
        #convertendo gabarito
        temp = []
        for i in gabarito:
            temp.append(tuple(i))
        gabarito = temp
        
        #miss = set(gabarito) - set(correct)
        
        miss = set()
        for ga in (set(gabarito) - set(correct)):
            for answer in correct:
                    if ( answer[0] == ga[1] and answer[1] == ga[0]):
                        pass
                    else:
                        if (gs_inverted_flag):
                            miss.add((ga[1],ga[0]))
                        else:
                            miss.add(ga)
        miss =  list(miss)
                            
            
            
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
        config.writeCompResult2csv(outfile,prof_d,dt1,p1,dt2,p2,
                                   len(correct),len(wrong),
                                   len(gabarito),list(miss),wrong)
        
        sfn = file.split('_')
        profile_dir = 'data/profile/'
        fn1 = sfn[2] +'_'+ sfn[3] +'_'+ sfn[4] +'_'+ sfn[5] + '.csv'
        fn2 = sfn[6] +'_'+ sfn[7] +'_'+ sfn[8] +'_'+ sfn[9]
        
        from util import csvutil
        rows_f1 = csvutil.read(profile_dir+fn1,delimiter=";",headers=True)
        rows_f2 = csvutil.read(profile_dir+fn2,delimiter=";",headers=True)
        
        
        r_tm = montaResultados2(correct,d,h,v,rows_f1,rows_f2,'TM')
        r_tnm = montaResultados2(miss,d,h,v,rows_f1,rows_f2,'TNM')
        r_fm = montaResultados2(wrong,d,h,v,rows_f1,rows_f2,'FM')
        
        
        
        rf = r_fm+r_tnm+r_tm
        r2 = r2 + rf
    
    r2 = [headers_r2] + r2
    config.write(r2_outfile,headers_r2,r2,result=True)
            
            
    
    print("=========== MISSED ===========")
    print(missed)
    print("=========== MOST WRONG ===========")
    print(most_wrong)
    print('Done!')