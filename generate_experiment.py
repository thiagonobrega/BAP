'''
Created on 17 de mar de 2017

@author: Thiago
python3 generate_experiments.py /home/thiagonobrega/Documents/data_01/
'''
import argparse

def check(dirToScreens):
    import os
    from os import path
    files = []
    for f in os.listdir(dirToScreens):
        if f.endswith(".csv"):
            files.append(f)
    return files

def getDataType(fname):
    if 'ncvoter' in fname:
        return 'ncvoters'
    if 'medpos' in fname:
        return 'medicare'
    if 'INMT4AA1' in fname:
        return 'ncinmates'
    return ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run Experiments',
    )
    
    parser.add_argument('dir', action="store", help='dir to scan')
    args = parser.parse_args()
    
    args_dir = args.dir
    files = check(args_dir)
    
    done_list = []
    for file1 in files:
        for file2 in files:
            if file1 != file2:
                dt1 = file1.split('_')[0].split('-')[0]
                dt2 = file2.split('_')[0].split('-')[0]
                
                if dt1 != dt2:                    
                    ok = True
                    for done in done_list:
                        if ( (done[0]==file1 or done[1]==file1) and (done[0]==file2 or done[1]==file2) ):
                            ok = False
                    
                    if ok:
                        p1 = 'python3 main_simcalc.py '
                        f1 = args_dir + file1 + ' '
                        f2 = args_dir + file2 + ' '
                        t1 = '-t1 ' + getDataType(file1)
                        t2 = ' -t2 ' + getDataType(file2)
                        if getDataType(file1) != getDataType(file2):
                            done_list.append([file1,file2])
                            print(p1+f1+f2+t1+t2)
    pass