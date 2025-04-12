from typing import List 
from os import fsync

from database import Database
from env import PATH, TOMBSTONE, META_STORAGE_PATH







def list_of_databases() -> List[str]:
    with open(f'{META_STORAGE_PATH}/list.txt', 'r') as f:
        names = [i.rstrip('\n') for i in f.readlines()]
    return names 





class Cluster:

    """
    Collection of all Nano databases 
    """

    def __init__(self) -> None: 
        """ Initialize the Cluster when the server starts running """
        self.names: List[str] = list_of_databases()
        print(self.names)
        self.current = Database("default") 
        self.len: int = len(self.names)
        self.recover_from_crash()


    def __contains__(self, name: str) -> bool:
        return name in self.names


    def create(self, name: str) -> str:
        self.names.append(name)
        self.len += 1 
        with open(f'{PATH}/storage/meta/wal.log', 'a') as f:
            print(name, file=f, flush = True)
            fsync(f.fileno())
        return f"OK. Created new database {name}"


    def drop(self, name: str) -> str:
        if name == self.current.name:
            self.current = Database("default")

        for i in range(self.len):
            if self.names[i] == name:
                self.names.pop(i)
                self.len -= 1 
                with open(f'{PATH}/storage/meta/wal.log', 'a') as f:
                    print(name, TOMBSTONE, file=f, flush = True)
                    fsync(f.fileno())
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
        with open(f'{PATH}/storage/meta/list.txt', 'w') as f:
            self.names = sorted(set(self.names))
            print('\n'.join(self.names), file = f) 
        f = open(f'{PATH}/storage/meta/wal.log', 'w')
        f.close()

    def recover_from_crash(self) -> None:
        with open(f'{PATH}/storage/meta/wal.log','r') as f:
            values = [tuple(i.rstrip('\n').split()) for i in f.readlines()]
            fixed = [x[0] for x in sorted(list(filter(lambda i : len(i) == 1, set(values))))]
        with open(f'{PATH}/storage/meta/list.txt', 'w') as f:
            print('\n'.join(fixed), file = f) 
