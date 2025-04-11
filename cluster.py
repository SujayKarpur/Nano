from typing import List, Optional 

from src import redblacktree
from database import Database
from meta_server import list_of_databases
from env import PATH, TOMBSTONE



class Cluster:

    def __init__(self) -> None: 
        self.names: List[str] = list_of_databases()
        self.current = Database("default") 
        self.len: int = len(self.names)


    def __contains__(self, name: str) -> bool:
        return name in self.names


    def create(self, name: str) -> str:
        self.names.append(Database(name))
        self.len += 1 
        with open(f'{PATH}/storage/meta/list.txt', 'a') as f:
            print(name, file=f)
        return f"OK. Created new database {name}"


    def drop(self, name: str) -> str:
        if name == self.current.name:
            return "Can't delete currently selected database"

        for i in range(self.len):
            if self.names[i] == name:
                self.names.pop(i)
                self.len -= 1 
                with open(f'{PATH}/storage/meta/list.txt', 'a') as f:
                    print(name, TOMBSTONE, file=f)
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
                return f"OK. Selected database {i.name}"
        else:
            return f"ERROR: No database {name} exists"
        

    def cleanup(self) -> None:
        pass 

    def recover_from_crash(self) -> None:
        pass 