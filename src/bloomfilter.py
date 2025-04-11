from mmh3 import hash # type: ignore
from bitarray import bitarray


from env import FLUSH_SIZE


BITARRAY_SIZE = 10000


class BloomFilter:

    def __init__(self, string=None):
        self.n: int = 0  
        self.m: int = BITARRAY_SIZE
        self.k = 7 
        if not string:
            self.array = bitarray(self.m)
            self.array.setall(0)
        else:
            self.array = bitarray(string)
        self.hash_functions = [(lambda i : hash(i, seed = x)) for x in range(self.k)]


    def insert(self, key: str) -> None: 
        for hash_function in self.hash_functions:
            self.array[hash_function(key) % BITARRAY_SIZE] = 1 
         

    def __contains__(self, key: str) -> bool:
        for hash_function in self.hash_functions:
            if not self.array[hash_function(key) % BITARRAY_SIZE]:
                return False 
        return True 

    def __repr__(self) -> str:
        return self.array.__repr__()