import os 

from src.redblacktree import RedBlackTree 
from env import PATH 


class WAL:

    def __init__(self, name: str):
        self.name = name 
        self.file_name = f'{PATH}/storage/{self.name}/wal.log'
        self.file = open(self.file_name, 'a') 
        self.file_open = True 
    
    def write(self, command: str):
        if not self.file_open:
            self.file = open(self.file_name, 'a')
            self.file_open = True 
        print(command, file = self.file, flush=True)
        os.fsync(self.file.fileno()) 

    def reset(self):
        if self.file_open:
            self.file.close()
        self.file = open(self.file_name, 'w')
        self.file.close()
        self.file_open = False  


    def close(self):
        if self.file_open:
            self.file.close() 
        self.file_open = False 
