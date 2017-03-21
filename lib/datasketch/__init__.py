"""
Data sketch module for Python
=============================

datasketch is a Python module integrating various data sketch
algorithms. It aims to provide efficient approximation alternatives
to exact solutions to data mining and data integration problems.
"""
from lib.datasketch.hyperloglog import HyperLogLog, HyperLogLogPlusPlus
from lib.datasketch.minhash import MinHash
from lib.datasketch.b_bit_minhash import bBitMinHash
from lib.datasketch.lsh import MinHashLSH, WeightedMinHashLSH
from lib.datasketch.weighted_minhash import WeightedMinHash, WeightedMinHashGenerator
