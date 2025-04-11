import os 

from src.redblacktree import RedBlackTree 
from env import PATH 


class WAL:

    def __init__(self, name: str, clusterlogger = False):
        self.name = name 
        self.file_name = f'{PATH}/storage/{self.name}/wal.log' if not clusterlogger else f''
        self.file = open(self.file_name, 'a') 
        self.file_open = True 
    
    def write(self, command: str):
        if not self.file_open:
            self.file = open(self.file_name, 'a')
            self.file_open = True 
        print(command, file = self.file) 

    def reset(self):
        if self.file_open:
            self.file.close()
        self.file = open(self.file_name, 'w')
        self.file_open = True 

    
    def open(self):
        if not self.file_open:
            self.file = open(self.file_name, 'a')
        self.file_open = True 

    def close(self):
        if self.file_open:
            self.file.close() 
        self.file_open = False 
