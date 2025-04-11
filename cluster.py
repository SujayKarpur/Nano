from typing import List, Optional 

from src import redblacktree
from database import Database


class Cluster:

    def __init__(self) -> None: 
        self.databases: List[Database] = [Database("default")]
        self.current: Database = self.databases[-1]
        self.len: int = 0 


    def __contains__(self, name: str) -> bool:
        return name in [s.name for s in self.databases]


    def create(self, name: str) -> str:
        self.databases.append(Database(name))
        self.len += 1 
        return f"OK. Created new database {name}"


    def drop(self, name: str) -> str:

        if name == self.current.name:
            return "Can't delete currently selected database"

        for i in range(self.len):
            if self.databases[i].name == name:
                self.databases.pop(i)
                self.len -= 1 
                return f"OK. Deleted database {name}"
        else:
            return f"ERROR: No database {name} exists"


    def list(self) -> str:
        return '\n'.join([s.name for s in self.databases])


    def select(self, name: str) -> str:
        for i in self.databases:
            if i.name == name:
                self.current.wal.close()
                self.current = i 
                return f"OK. Selected database {i.name}"
        else:
            return f"ERROR: No database {name} exists"
        

    def cleanup(self) -> None:
        pass 