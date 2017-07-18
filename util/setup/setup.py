'''
Created on 23 de abr de 2016

@author: Thiago
'''
import pip


def install(package):
    pip.main(['install', package])

def update(package):
    pip.main(['update', package])
    
def upgradePiP():
    pip.main(['upgrade', 'pip'])

def upgrade(package):
    pip.main(['install','--upgrade' ,package])
        
if __name__ == '__main__':
    install('simhash')
    import sys
    sys.exit()
    upgrade('setuptools')
    upgrade('pip')
# pyblomm
    install('ngram')
    install('bitarray')
    install('xxhash')
    
    upgrade('ngram')
    upgrade('bitarray')
    upgrade('xxhash')
    
    #debug memoria
    install('pympler')

#
    #install('pybloom')
#     install("numpy")
#     upgrade('pybloom')
    