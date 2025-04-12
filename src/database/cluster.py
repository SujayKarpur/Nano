from typing import List 
from os import fsync
from bisect import insort, bisect 
import json 

from src.database.wal import WAL 
from src.database.database import Database
from src.user.user import User 

import env



LIST_PATH = f'{env.META_STORAGE_PATH}/list.txt'
LOG_PATH = f'{env.META_STORAGE_PATH}/wal.log'




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
        self.wal = WAL(env.META_STORAGE_PATH)
        self.current = Database("default") 
        self.len: int = len(self.names)
        env.current_database = Database("default")
        self.recover_from_crash()


    def __contains__(self, name: str, user: User) -> bool:
        return name in set.intersection(set(self.names), set(user.read()))


    def create(self, name: str, user: User) -> str:
        self.names.append(name)
        self.len += 1 
        self.wal.write(name)

        with open(f'{env.USER_STORAGE_PATH}/{user.username}.json', 'r') as f:
            dbs = json.load(f) 
        
        dbs[name] = 4 

        with open(f'{env.USER_STORAGE_PATH}/{user.username}.json', 'w') as f:
            dbs = json.dump(dbs, f, indent=2)

        return f"OK. Created new database {name}"


    def drop(self, name: str, user: User) -> str:
        if name == self.current.name:
            env.current_database = Database("default")
            self.current = Database("default")

        for i in range(self.len):
            if self.names[i] == name:
                self.names.pop(i)
                self.len -= 1 
                self.wal.write(f'{name} {env.TOMBSTONE}')

                with open(f'{env.USER_STORAGE_PATH}/{user.username}.json', 'r') as f:
                    dbs = json.load(f) 
                
                dbs.pop(name)

                with open(f'{env.USER_STORAGE_PATH}/{user.username}.json', 'w') as f:
                    dbs = json.dump(dbs, f, indent=2)

                return f"OK. Deleted database {name}"
            

        else:
            return f"ERROR: No database {name} exists"


    def list(self, user: User) -> str:
        return '\n'.join(self.names)


    def select(self, name: str, user: User) -> str:
        for i in self.names:
            if i == name:
                self.current.db.shutdown()
                self.current = Database(i)
                env.current_database = Database(i)
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
