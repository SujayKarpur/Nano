from typing import Tuple


from src.redblacktree import RedBlackTree 
from src.wal import WAL 
from src.bloomfilter import BloomFilter
from src.memtable import Memtable
from src.sstable import SSTable

from env import FLUSH_SIZE




class LSMTree:

    def __init__(self, name: str) -> None:
        self.name = name  
        self.memtable = Memtable(self.name)
        self.sstable = SSTable(self.name)

    
    def startup(self) -> None:
        pass 

    def shutdown(self) -> None:
        self.sstable.write(self.memtable) 


    def set(self, key: str, value: str) -> bool: 
        inserto = self.memtable.set(key, value) 
        if not inserto:
            return False 
        if self.memtable.number_of_elements > FLUSH_SIZE:
            self.sstable.write(self.memtable)
            self.memtable = Memtable(self.name)
        return True 


    def get(self, key: str) -> Tuple[bool,str]:
        exists, value = self.memtable.get(key)
        if exists:
            return exists, value 
        else:
            return self.sstable.find(key)


    def delete(self, key: str) -> bool:
        exists, _ = self.get(key)
        if not exists:
            return False 
        else:
            self.memtable.delete(key)  
