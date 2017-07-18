'''
Created on 20 de abr de 2017

@author: Thiago
'''

from lib.datasketch import minhash
from lib import simhash


mh1 = minhash.MinHash()
att = 'a'

mh1.update(att.encode('utf8'))

print(mh1.digest())