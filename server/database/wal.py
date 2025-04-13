import os 

from server.env import PATH 


class WAL:

    """
    Write Ahead Log
    """

    def __init__(self, directory_path: str):
        self.file_name = f'{directory_path}/wal.log'
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
