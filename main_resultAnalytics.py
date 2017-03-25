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

if __name__ == '__main__':
    #file = 'C:\\Users\\Thiago\\Desktop\\result_comp_ncvoter_random_selected_0_medpos_random_selected_0.csv'
    
    #h,v,d = minhash_util.read_minhashCompResult(file)
    #results = minhash_util.getResults(h,v,d,limiar_l=0.9)
    #correct, wrong = minhash_util.evaluateResults(h,v,results)
    #data = minhash_util.list_2d_dict(h,v,d)
    #f = 'result_comp_medpos_random_selected_0.075p_INMT4AA1_random_selected_0.0025p.csv'
    di = 'F:\\results\\18032017\\'
    di = 'F:\\results\\22032017\\'
    #di = 'F:\\results\\debug\\'
    outfile = 'data/18032017.csv'
    outfile = 'data/22032017.csv'
    
    files = check(di)
    for file in files:
        h,v,d = minhash_util.read_minhashCompResult(di + file)
        results = minhash_util.getResults(h,v,d,limiar_l=0.5)
        
        correct, wrong ,gabarito = minhash_util.evaluateResults(h,v,results)
        
        line = file.split('_')
        dt1 = line[2]
        p1 = line[5]
        dt2 = line[6]
        p2 = line[9].split('.csv')[0]
        
        prof_d = config.readDataProfile2Dict('data\profile.csv')
        config.writeCompResult2csv(outfile,prof_d,dt1,p1,dt2,p2,
                                   len(correct),len(wrong),
                                   gabarito)
    
    print('Done!')