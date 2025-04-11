from typing import List, Tuple 

from src.redblacktree import RedBlackTree, TraversalType
from src.bloomfilter import BloomFilter 
from src.wal import WAL 
from src.memtable import Memtable

from env import PATH, FLUSH_SIZE


class DataBlock:
    
    def __init__(self, name: str, count: int) -> None:
        self.name = name 
        self.count = count 
        self.file_name = f'{PATH}/storage/{name}/sstable_datablock_{count}' 

    def write(self, data: Memtable) -> None:
        with open(self.file_name, 'w') as f:
            for node in data.ordered_list():
                print(node.key, node.value, file = f)

    def find(self, key: str) -> Tuple[bool,str]:
        pass 



class MetaBlock:

    def __init__(self, data: Memtable, name: str, count: int) -> None:
        self.data = data 
        self.name = name 
        self.count = count 
        self.file_name = f'{PATH}/storage/{name}/sstable_metablock_{count}' 

    
    def write(self, data: Memtable):
        pass 

    def find(self, key: str) -> Tuple[bool,str]:
        pass 




class SSTable:

    def __init__(self, name: str) -> None:
        self.number_of_blocks = 0  
        self.name = name 

    def flush(self, ) -> None:
        pass 

    def get(self, key: str) -> None:
        pass 

    