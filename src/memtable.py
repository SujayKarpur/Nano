from typing import Tuple, List  

from src.redblacktree import RedBlackTree, TraversalType, Node
from src.bloomfilter import BloomFilter 
from src.wal import WAL 
from env import FLUSH_SIZE, TOMBSTONE



class Memtable:

    def __init__(self, name: str):
        self.name = name 
        self.data = RedBlackTree()
        self.wal = WAL(self.name)
        self.number_of_elements = 0 


    def set(self, key: str, value: str) -> bool:

        if value == TOMBSTONE:
            return False 

        self.data.insert(key, value)
    
        self.wal.write(f"SET {key} {value}")
        self.number_of_elements += 1
        return True  


    def get(self, key: str) -> Tuple[bool, str]:
        if key in self.data:
            return (True, self.data.get(key).value)
        else:
            return (False, '')


    def delete(self, key: str) -> bool:
        self.data.insert(key, TOMBSTONE) #tom
        self.wal.write(f"DELETE {key}")
        return True 
    

    def startup(self) -> None:
        self.replay()  


    def shutdown(self) -> None:
        self.wal.reset() 


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



    def ordered_list(self) -> List[Node]:
        return self.data.traverse(TraversalType.INORDER)