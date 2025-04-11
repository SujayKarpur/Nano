from typing import Tuple


from src.redblacktree import RedBlackTree 
from src.wal import WAL 
from src.bloomfilter import BloomFilter
from src.memtable import Memtable
from src.sstable import SSTable




class LSMTree:

    def __init__(self, name: str) -> None:
        self.name = name  
        self.memtable = Memtable(name)
        self.sstable = SSTable(name)

    
    def startup(self) -> None:
        pass 

    def shutdown(self) -> None:
        pass 


    def set(self, key: str, value: str) -> bool: 
        pass 


    def get(self, key: str) -> Tuple[bool,str]:
        pass 


    def delete(self, key: str) -> bool:
        pass  
