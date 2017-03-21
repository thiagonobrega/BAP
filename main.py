# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:11:16 2017

@author: Thiago Nobrega
"""

import csv
import random 
import time


    
if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser(
        description='Example with nonoptional arguments',
    )
    parser.add_argument('file', action="store", help='Original file')

    parser.add_argument('-p', action='append',
                        dest='percents',
                        default=[],
                        help='Generate a newsubset with a -p percent of original dataset')
    
    args = parser.parse_args()
    
    