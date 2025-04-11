import os 

from src.redblacktree import RedBlackTree 
from env import PATH 


class WAL:

    def __init__(self, name: str):
        self.name = name 
        self.file = open(f'{PATH}/storage/{self.name}/wal.log', 'a') 
    
    def write(self, command: str):
        print(command, file = self.file) 

    def replay(self):
        pass 

    def reset(self):
        self.file.close()
        self.file = open(f'../storage/{self.name}/wal.log', 'w')

    def close(self):
        self.file.close() 