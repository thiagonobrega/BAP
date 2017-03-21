'''
Created on 4 de mar de 2017

@author: Thiago Nobrega
@contact: thiagonobrega@gmail.com
@version: 0.0.1

'''

import os

class Slicer(object):
    '''
    classdocs
    
    thanks to Alistair Martin (http://www.blopig.com/blog/2016/08/processing-large-files-using-python/)

    '''
#     @classmethod
    def chunkify(self):
        import codecs    
        fileEnd = os.path.getsize(self.file)
        with codecs.open(self.file,encoding=self.file_encoding) as f:
#         with open(self.file) as f:
            
            chunkEnd = f.tell()
            while True:
                chunkStart = chunkEnd
#                 com codecs
                f.seek(self.chunk_size,1)
#                 f.seek(self.chunk_size,0)
#                 f.readline()
                pos = Slicer._EOC(f)
                chunkEnd = f.tell()
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break
    
    
    @staticmethod
    def _EOC(f):
    
        l = f.readline()#incomplete line
        p = f.tell()
        if not l: return #EOF
        
        l = f.seek(p-500)
        
#         alterar para linux
        eol = '\n'
        es = 0
#         os.linesep
        import os
        while (es == 0):
            if (l == eol):
                es = 1
                f.seek(p)
                return p
            else:
#                 atletar para linux
                l = f.read(1)
                p = f.tell()
            
        p = f.tell()
        f.seek(p)

    #read chunk
#     @staticmethod
    def read(self,chunk):    
#         with open(self.file,'r',) as f:
        with open(self.file,encoding=self.file_encoding) as f:
            f.seek(chunk[0])
            return f.read(chunk[1])
    
     #iterator that splits a chunk into units
    @staticmethod
    def parse(chunk):
        for line in chunk.splitlines():
            yield chunk


    def __init__(self, filepath , file_encoding="UTF-8" , chunk_size_mb=1):
        '''
        Constructor
        '''
        
        self.file = filepath
        print(self.file)
        self.file_encoding = file_encoding
        self.chunk_size = int(chunk_size_mb * (1024*1024))
        