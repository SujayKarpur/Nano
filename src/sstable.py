from typing import List, Tuple 
import linecache
import asyncio 

from src.redblacktree import RedBlackTree, TraversalType
from src.bloomfilter import BloomFilter 
from src.wal import WAL 
from src.memtable import Memtable

from env import PATH, FLUSH_SIZE


class DataBlock:
    
    def __init__(self, name: str, count: int, data: Memtable) -> None:
        self.data = data
        self.name = name 
        self.count = count 
        self.file_name = f'{PATH}/storage/{name}/sstable_datablock_{count}' 

        with open(self.file_name, 'w') as f:
            for node in data.ordered_list():
                print(node.key, node.value, file = f)


    def find(self, key: str) -> Tuple[bool,str]:
        pass 



class MetaBlock:

    def __init__(self, name: str, count: int, data: Memtable) -> None:
        self.data = data 
        self.name = name 
        self.count = count 
        self.file_name = f'{PATH}/storage/{name}/sstable_metablock_{count}' 

        bf = BloomFilter()

        ol = data.ordered_list()
        min_key = ol[0]; max_key = ol[-1]

        for node in ol:
            bf.insert(node.key)


        with open(self.file_name, 'w') as f:
            print(bf, file=f)
            print(min_key, max_key, file=f)
            print(data.number_of_elements, file=f)




    def find(self, key: str) -> Tuple[bool,str]:
        
        with open(self.file_name, 'r') as f:
            contents = [i.rstrip('\n') for i in f.readlines()]
            filter_string = contents[0]
            bf = BloomFilter(filter_string)
            if key not in bf:
                return (False, '')
            min_key, max_key = contents[1].split()
            if key < min_key or key > max_key:
                return False 
            n = int(contents[2])
            return #search in the corresponding data file 


class SSTable:

    def __init__(self, name: str) -> None:
        self.number_of_blocks = 0  
        self.name = name 

    def flush(self, ) -> None:
        pass 

    def get(self, key: str) -> None:
        pass 

    