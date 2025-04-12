from typing import List 
from os import fsync
from bisect import insort, bisect 

from src.wal import WAL 
from database import Database
from env import PATH, TOMBSTONE, META_STORAGE_PATH



LIST_PATH = f'{META_STORAGE_PATH}/list.txt'
LOG_PATH = f'{META_STORAGE_PATH}/wal.log'




def list_of_databases() -> List[str]:
    with open(LIST_PATH, 'r') as f:
        names = [i.rstrip('\n') for i in f.readlines()]
    return names 





class Cluster:

    """
    Collection of all Nano databases 
    """

    def __init__(self) -> None: 
        """ Initialize the Cluster when the server starts running """
        self.names: List[str] = list_of_databases()
        self.wal = WAL(META_STORAGE_PATH)
        self.current = Database("default") 
        self.len: int = len(self.names)
        self.recover_from_crash()


    def __contains__(self, name: str) -> bool:
        return name in self.names


    def create(self, name: str) -> str:
        self.names.append(name)
        self.len += 1 
        self.wal.write(name)
        return f"OK. Created new database {name}"


    def drop(self, name: str) -> str:
        if name == self.current.name:
            self.current = Database("default")

        for i in range(self.len):
            if self.names[i] == name:
                self.names.pop(i)
                self.len -= 1 
                self.wal.write(f'{name} {TOMBSTONE}')
                return f"OK. Deleted database {name}"
        else:
            return f"ERROR: No database {name} exists"


    def list(self) -> str:
        return '\n'.join(self.names)


    def select(self, name: str) -> str:
        for i in self.names:
            if i == name:
                self.current.db.shutdown()
                self.current = Database(i)
                return f"OK. Selected database {i}"
        else:
            return f"ERROR: No database {name} exists"
        

    def cleanup(self) -> None:
        with open(LIST_PATH, 'w') as f:
            self.names = sorted(set(self.names))
            print('\n'.join(self.names), file = f) 
        self.wal.reset()

    def recover_from_crash(self) -> None:
        with open(LOG_PATH,'r') as f:
            lines = [i.rstrip('\n') for i in f.readlines()]
            databases = set()
            for i in lines:
                if len(i.split()) == 1:
                    databases.add(i)
            #values = [tuple(i.rstrip('\n').split()) for i in f.readlines()]
            #fixed = [x[0] for x in sorted(list(filter(lambda i : len(i) == 1, set(values))))]
        with open(LIST_PATH, 'w') as f:
            print('\n'.join(databases), file = f) 
