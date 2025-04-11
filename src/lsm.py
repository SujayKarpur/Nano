from typing import Tuple
import os 


from src.redblacktree import RedBlackTree 
from src.wal import WAL 
from src.bloomfilter import BloomFilter
from src.memtable import Memtable
from src.sstable import SSTable

from env import FLUSH_SIZE, PATH 




def how_many_blocks(name: str) -> int:
    """ how many SSTable data/meta blocks already exist? """
    return len(list(filter(lambda i : 'sstable_datablock_' in i, os.listdir(os.path.join(PATH + '/storage', name))))) 




class LSMTree:

    """
    Implementation of a Log-Structured Merge Tree 
    """

    def __init__(self, name: str) -> None:
        self.name = name  
        self.memtable = Memtable(self.name)
        self.sstable = SSTable(self.name, how_many_blocks(self.name))

    
    def startup(self) -> None:
        """ run this upon starting """
        self.memtable.startup()
         

    def shutdown(self) -> None:
        """ run this when the user exits """
        self.memtable.shutdown()
        self.sstable.flush(self.memtable) 


    def set(self, key: str, value: str) -> bool: 
        """ set database[key] = val """

        inserto = self.memtable.set(key, value) 
        if not inserto:
            return False 
        if self.memtable.number_of_elements > FLUSH_SIZE:
            self.sstable.write(self.memtable)
            self.memtable = Memtable(self.name)
        return True 


    def get(self, key: str) -> Tuple[bool,str]:
        """ get database[key] if it exists """

        exists, value = self.memtable.get(key)
        if exists:
            return exists, value 
        else:
            return self.sstable.get(key)


    def delete(self, key: str) -> bool:
        """ delete <key> from database """

        exists, _ = self.get(key)
        if not exists:
            return False 
        else:
            self.memtable.delete(key)  
