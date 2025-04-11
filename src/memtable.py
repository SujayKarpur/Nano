from src.redblacktree import RedBlackTree
from src.bloomfilter import BloomFilter 
from src.wal import WAL 
from env import FLUSH_SIZE



class Memtable:

    def __init__(self, name: str):
        self.name = name 
        self.data = RedBlackTree()
        self.wal = WAL(self.name)


    def set(self, key: str, value: str) -> bool:
        self.data.insert(key, value)
        if self.data.size > FLUSH_SIZE:
            pass 
        return True  


    def get(self, key: str) -> bool:
        pass 


    def delete(self, key: str) -> bool:
        pass  





    def replay(self) -> None:
        pass 


    def flush(self) -> None:
        pass 

    
    

    def select(self) -> None:
        pass 


    def deselect(self) -> None:
        pass 