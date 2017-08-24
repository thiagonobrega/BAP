'''
Created on 31 de jul de 2017

@author: Thiago Nobrega
'''

import time
import argparse
import csv
import pandas as pd
import numpy as np
import scipy as sp
from util import config
from datetime import datetime

def check(dirToScreens):
    import os
    from os import path
    files = []
    for f in os.listdir(dirToScreens):
        if f.endswith(".csv"):
            files.append(f)
    return files


#TODO REVER O RATTING
def convert_reviewTrip(dir_in,dir_out,file_in):
    '''
        Data pre-processing step to trip_advisor reviews
    '''
    
    headers = ['restaurant'] 
    adress_labels = ['streetAddress', 'addressLocality', 'addressRegion_State', 'postalCode','Country']
    review_labels = ['author','ratingValue','datePublished','ratingValue_2','reviewBody','ratingValue_3']
    headers = headers + adress_labels + review_labels
    
    file = dir_in + file_in
    data = pd.read_csv(file, sep=",",header=None)
    data.columns = headers

    for i in range(0,len(data)):
        for j,header in enumerate(headers):
            if (str(data[header][i]).upper() == "NAN"):
                data.set_value(i,header,"")
            else:
                if (header == 'datePublished'):
                    dt = datetime.strptime(str(data[header][i]).upper(), '%B %d, %Y')
                    newdate = str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year) 
                    data.set_value(i,header,newdate)
                else:
                    data.set_value(i,header,str(data[header][i]).upper())
    
    del data['ratingValue_2']
    del data['ratingValue_3']
    data['ratingValue'] = data['ratingValue'].astype(float)
    file_out = dir_out + file_in
    data.to_csv(file_out,index=False,encoding='utf-8',quoting=csv.QUOTE_ALL)

def convert_ohioVoters(dir_in,dir_out,file_in):
    '''
        Data pre-processing step to ohio voters
    '''
    
    file = dir_in + file_in
    data = pd.read_csv(file, sep=",")

    for i in range(0,len(data)):
        for j,header in enumerate(data.columns):
            if (str(data[header][i]) == "nan"):
                data.set_value(i,header,"")
            else:
                if ((header == 'birth_date') or (header == 'register_date')):
                    dt = datetime.strptime(str(data[header][i]), '%Y-%m-%d')
                    newdate = str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year) 
                    data.set_value(i,header,newdate)
    
    file_out = dir_out + file_in
    data.to_csv(file_out,index=False,encoding='utf-8',quoting=csv.QUOTE_ALL)

def convert_ncVoters(dir_in,dir_out,file_in):
    '''
        Data pre-processing step to nc voters
    '''
    
    file = dir_in + file_in
    data = pd.read_csv(file, sep=",")
    data['mail_zipcode'] = data['mail_zipcode'].map('{:.0f}'.format)
    
    for i in range(0,len(data)):
        for j,header in enumerate(data.columns):
            if (str(data[header][i]) == "nan"):
                data.set_value(i,header,"")
            else:
                if (header == 'registr_dt'):
                    dt = datetime.strptime(str(data[header][i]), '%m/%d/%Y')
                    newdate = str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year) 
                    data.set_value(i,header,newdate)
                    
    file_out = dir_out + file_in
    data.to_csv(file_out,index=False,encoding='utf-8',quoting=csv.QUOTE_ALL)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Executa a comparacao (calculo de similaridade) de todos os arquivos em um diretorio',
    )
    
    parser.add_argument('dir', action="store", help='Input dir')
    
    parser.add_argument('output_dir', action="store", help='Output dir')

    parser.add_argument('-i', action="store",dest="format",
                        help='input format:\n' + 
                        '- RESTAURANTS \n\t - reviews_trip' + 
                        '\n - VOTERS \n\t - ohio_voters \n\t - nc_voters')
    
    args = parser.parse_args()
        
    input_dir = args.dir
    input_format = args.format
    output_dir = args.output_dir
    
    import os
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass
    
    #start_h = time.time()
    #end_h = time.time()
    #config.writeExecTime2csv(file,"BIGRAM_CALC"+str(encrypt),start_h,end_h)
    
    if input_format == "reviews_trip":
        print("EXECUTING : " + input_format )
        for file in check(input_dir):
            start_sf = time.time()
            convert_reviewTrip(input_dir, output_dir, file)
            end_sf = time.time()
            config.writeExecTime2csv(file,"STANDARD_FROMAT ["+str(input_format)+"]",start_sf,end_sf)
    
    if input_format == "general_trip":
        print("ERROR: NAO IMPLEMENTADO")
    
    if input_format == "ohio_voters":
        print("EXECUTING : " + input_format )
        for file in check(input_dir):
            start_sf = time.time()
            convert_ohioVoters(input_dir, output_dir, file)
            end_sf = time.time()
            config.writeExecTime2csv(file,"STANDARD_FROMAT ["+str(input_format)+"]",start_sf,end_sf)
    
    if input_format == "nc_voters":
        print("EXECUTING : " + input_format )
        for file in check(input_dir):
            start_sf = time.time()
            convert_ncVoters(input_dir, output_dir, file)
            end_sf = time.time()
            config.writeExecTime2csv(file,"STANDARD_FROMAT ["+str(input_format)+"]",start_sf,end_sf)
    
                