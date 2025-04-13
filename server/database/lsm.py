from typing import Tuple
import os 


from server.database.memtable import Memtable
from server.database.sstable import SSTable

from server.env import FLUSH_SIZE, STORAGE_PATH




def how_many_blocks(name: str) -> int:
    """ how many SSTable data/meta blocks already exist? """
    # logic:
    #1 - find the directory 
    #2 - check the number of files in the directory
    #3 - filter to include only 1 file per logical block 
    #4 - return the length of that list 

    files_in_dir = os.listdir(name)
    filtered_files = list(filter(lambda i : 'sstable_datablock_' in i, files_in_dir))
    return len(filtered_files)

    #return len(list(filter(lambda i : 'sstable_datablock_' in i, os.listdir(os.path.join(PATH + '/storage', name))))) 




class LSMTree:

    """
    Implementation of a Log-Structured Merge Tree 
    """

    def __init__(self, owner: str, name: str) -> None:
        """
        Initialize the LSM tree with the parameter `name`, which is the name of the database 
        """
        self.owner = owner 
        self.name = name  
        self.path = f'{STORAGE_PATH}/{self.owner}/databases/{name}'
        self.memtable = Memtable(self.path)
        self.sstable = SSTable(self.path, how_many_blocks(self.path))

    
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

        self.memtable.temporary_replay()
        exists, value = self.memtable.get(key)
        if exists:
            return exists, value 
        else:
            print("CHECKING SSTABLE!!")
            return self.sstable.get(key)


    def delete(self, key: str) -> bool:
        """ delete <key> from database """

        exists, _ = self.get(key)
        if not exists:
            return False 
        else:
            self.memtable.delete(key)  
