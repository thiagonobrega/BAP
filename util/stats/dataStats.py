'''
Created on 2 de mar de 2017

@author: Thiago Nobrega
@mail: thiagonobrega@gmail.com

iconv -t UTF-8 YourFile.txt

 iconv -f ISO-8859-1 -t UTF-8 ncvoter.csv > n.csv
 thanks to Alistair Martin (http://www.blopig.com/blog/2016/08/processing-large-files-using-python/)
'''

import multiprocessing
import csv
from io import StringIO
from util.slicer import Slicer
import pandas as pd
import numpy as np
      
def list2array(mylist,rs):
    print(rs)
    array = np.zeros((len(mylist),rs))
    i = 0
    for e in mylist:
        if len(e) ==5:
            print(i,e)
        array[i,] = e
        i += 1
    return array

def start_process():
    print('Starting', multiprocessing.current_process().name)


def exec_wrap(data):
    return run(data[0],data[1],data[2],data[3],data[4])

def run(slicer,slice,headers,first,rowsize):
    
    sdata = StringIO(slicer.read(slice))
    
    print(slice)
    reader = csv.reader(sdata,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL, skipinitialspace=True)
    
    if (first):
        next(reader, None)
        
    
    data_stats = []
    
    
    
    for row in reader:
        row_size = len(row)
        #stat_line = np.zeros((1,row_size),dtype=np.int16)
        stat_line = []
        
        for column in range(0,row_size):
            stat_line.append( len(str(row[column])) )
            
        try:
#             data_stats.loc[len(data_stats)] = stat_line
            if(rowsize == row_size):
                data_stats.append(stat_line)
            else:
                print('======== erro =======')
                print(row)
        except ValueError:
            print(row)

    #return data_stats
    return list2array(data_stats,rowsize)
    #return np.array(data_stats,dtype=np.int16)
    #return np.reshape(data_stats, (len(data_stats),row_size))

if __name__ == '__main__':
    
    file = "F:\\temp\\e1\\saida.csv"
    
    s = Slicer(file,chunk_size_mb=0.1,file_encoding='utf_16_le')
    
    columns = [ 'voter_id' , 'lastname' , 'firstname' , 'midlname' , ' name_sufix' , 'gender' , 'age' ,
                'race' , 'ethinic' , 'county' , 'street' , 'city' , 'state' , 'zip' , 'phone' ,
                'birth_place' , 'register_date' , 'ncid' , 'mail_adddr1' , 'mail_addr2' ,
                'mail_city' , 'mail_state' , 'mail_zip']
    
    first = True    
    pool_size = multiprocessing.cpu_count() * 2
#     pool_size = 2
    
    pool = multiprocessing.Pool(processes=pool_size, initializer=start_process )
    
    job_args = []
                   
    for chunkStart,chunkSize in s.chunkify():
        
        slice = [chunkStart,chunkSize]
        
        print('Slice:' + str(slice[0]) + ',' +str(slice[1]) )
        
        if (first):
            job_args.append([s,slice,columns,True])            
            first = False
        else:
            job_args.append([s,slice,columns,False])
    
    
    pool_outputs = pool.map(exec_wrap, job_args )
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks
    
    r = pool_outputs[0]
    for rt in pool_outputs[1:]:
        r = np.concatenate((r,rt))
    df = pd.DataFrame(r)
    #del r
    
    result = {}
    result['headers'] = columns
    result['mean'] = df.mean()[1:]
    result['median'] = df.median()[1:]
    result['var'] = df.var()[1:]
    result['std'] = df.std(ddof=1).tolist()[1:]

#     print('Pool    :', pool_outputs)
        
    print ("Exiting Main Thread")