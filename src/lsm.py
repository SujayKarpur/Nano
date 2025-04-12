from typing import Tuple
import os 


from src.memtable import Memtable
from src.sstable import SSTable

from env import FLUSH_SIZE, PATH, STORAGE_PATH




def how_many_blocks(name: str) -> int:
    """ how many SSTable data/meta blocks already exist? """
    # logic:
    #1 - find the directory 
    #2 - check the number of files in the directory
    #3 - filter to include only 1 file per logical block 
    #4 - return the length of that list 

    required_directory = os.path.join(STORAGE_PATH, name)
    files_in_dir = os.listdir(required_directory)
    filtered_files = list(filter(lambda i : 'sstable_datablock_' in i, files_in_dir))
    return len(filtered_files)

    #return len(list(filter(lambda i : 'sstable_datablock_' in i, os.listdir(os.path.join(PATH + '/storage', name))))) 




class LSMTree:

    """
    Implementation of a Log-Structured Merge Tree 
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the LSM tree with the parameter `name`, which is the name of the database 
        """
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

        inserto = self.memtable.set(key, value) #inserto == False iff value == TOMBSTONE (tombstone value, not the string 'TOMBSTONE')
        if not inserto:
            return False 
        if self.memtable.number_of_elements > FLUSH_SIZE:
            self.sstable.flush(self.memtable)
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
