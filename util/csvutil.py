'''
Created on 15 de jun de 2016

@author: Thiago Nobrega
@mail: thiagonobrega@gmail.com
'''

import csv

def readQuoted(file, delimiter = '\t', headers = False):
    """"
        Read a csv file with comma
        delimiter : comma (,) default
        headers : include headers in return
        
        return : list of rows (list) e.g: [[id,name,date],[1,joao,21],[2,maria,19]]  
    """
    rows = []
    with open(file, 'r') as f:
        reader = csv.reader(f,delimiter=delimiter,quotechar='"',quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for row in reader:
            rows.append(row)
    if not headers:
        rows = rows[1:]
    return rows

def read(file, delimiter = ',', headers = False):
    """"
        Read a csv file with comma
        delimiter : comma (,) default
        headers : include headers in return
        
        return : list of rows (list) e.g: [[id,name,date],[1,joao,21],[2,maria,19]]  
    """
    rows = []
    with open(file, 'r' , encoding='utf-8') as f:
        reader = csv.reader(f,delimiter=delimiter)
        for row in reader:
            rows.append(row)
    if not headers:
        rows = rows[1:]
    return rows

def write(outfile,data,delimiter=';',encode='utf-8',writemode='w'):
    """"
        Write a csv file 
        data : a list of list to be 
        delimiter : dot comma (;) default  
        writemode a == apend
    """
    ofile  = open(outfile, writemode , encoding=encode)
    writer = csv.writer(ofile, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_NONE)
    #writer = csv.writer(ofile, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for row in data:
        writer.writerow(row)
    ofile.close()




# if __name__ == '__main__':
#     file = "C:\Users\Thiago\Dropbox\Mestrado\workspace\python\geko_br\geko\example-data-english.csv"
#     a = read(file,headers=True)
#     print(a[0][0])
#     print(len(a))
#     write("nada.csv",a)
#     b = read("nada.csv",headers=True,delimiter=";")
#     print(b)
#     write("bada.csv",b)