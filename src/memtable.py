from typing import Tuple, Any, Optional 

from src.redblacktree import RedBlackTree
from src.bloomfilter import BloomFilter 
from src.wal import WAL 
from env import FLUSH_SIZE, TOMBSTONE



class Memtable:

    def __init__(self, name: str):
        self.name = name 
        self.data = RedBlackTree()
        self.wal = WAL(self.name)


    def set(self, key: str, value: str) -> bool:

        if value == TOMBSTONE:
            return False 

        self.data.insert(key, value)

        if self.data.size > FLUSH_SIZE:
            pass 

        return True  


    def get(self, key: str) -> Tuple[bool, str]:
        if key in self.data:
            return (True, self.data.get(key).value)
        else:
            return (False, '')


    def delete(self, key: str) -> bool:
        if key in self.data:
            self.data.insert(key, TOMBSTONE) #tom
            return True 
        else:
            return False 




    def replay(self) -> None:
        self.wal.close()
        f = open(self.wal.file_name, 'r') 
        commands = [i.rstrip('\n') for i in f.readlines()]
        for command in commands:
            command_list = command.split()
            if command_list[0] == 'SET':
                self.set(command_list[1], command_list[2])
            elif command_list[0] == 'DELETE':
                self.delete(command_list[1])
        f.close()
        self.wal.reset()


    def flush(self) -> None:
        pass #if the size of the red-black tree > 1000, flush to an SSTable 

    
    

    def select(self) -> None:
        pass 


    def deselect(self) -> None:
        pass 