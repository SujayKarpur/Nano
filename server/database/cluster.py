from typing import List 
from os import makedirs 
from bisect import insort, bisect 
import json 
 

from server.database.wal import WAL 
from server.database.database import Database
from server.user.user import User 


from server.statehandler import get_current_username, get_current_db_name, set_current_db_name

from server import env



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

    def __init__(self, username: str) -> None: 
        """ Initialize the Cluster when the server starts running """
        self.startup()
        self.names: List[str] = list_of_databases()
        self.onames = self.names 
        self.delnames: List[str] = []
        self.wal = WAL(env.META_STORAGE_PATH)
        self.len: int = len(self.names)


        self.username = username 
        new_name = "default"+self.username

        self.user = User(self.username)
        makedirs(f'{env.DATABASE_STORAGE_PATH}/{new_name}', exist_ok = True)

        if new_name not in self.onames:
            self.create(new_name)

        self.current = Database(new_name) 
        set_current_db_name(new_name)

        if new_name not in self.names:
            self.names.append(new_name)

        self.names = list(set.intersection(set(self.names), set(self.user.read())) | {new_name})
 


    def __contains__(self, name: str) -> bool:
        if name == "default":
            return True 
        return name in set.intersection(set(self.names), set(self.user.read()))


    def create(self, name: str) -> str:
        self.names.append(name)
        self.len += 1 
        self.wal.write(name)

        with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'r') as f:
            dbs = json.load(f) 
        
        dbs[name] = 4 

        with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'w') as f:
            dbs = json.dump(dbs, f, indent=2)

        return f"OK. Created new database {name}"


    def drop(self, name: str) -> str:

        if name == self.current.name:
            set_current_db_name("default" + self.username)
            self.current = Database("default" + self.username)


        for i in range(self.len):
            if self.names[i] == name:
                self.names.pop(i)
                self.delnames.append(i)
                self.len -= 1 
                self.wal.write(f'{name} {env.TOMBSTONE}')

                with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'r') as f:
                    dbs = json.load(f) 
                
                dbs.pop(name)

                with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'w') as f:
                    dbs = json.dump(dbs, f, indent=2)

                return f"OK. Deleted database {name}"
            

        else:
            return f"ERROR: No database {name} exists"


    def list(self) -> str:
        print('hi i"m in list')
        print(set(self.names))
        print(set(self.user.read()))
        return '\n'.join((set.intersection(set(self.names), set(self.user.read())) | {"default"}) - {"default" + self.username})


    def select(self, name: str) -> str:

        if name == "default":
            name += self.username 


        if name == self.current.name:
            return f"Void. Already in database {name}"

        for i in self.names:
            if i == name:
                self.current.shutdown()
                self.current = Database(i)
                set_current_db_name(i)
                return f"OK. Selected database {i}"
        else:
            return f"ERROR: No database {name} exists"
        


    def shutdown(self) -> None:

        if self.current:
            self.current.shutdown()

        with open(LIST_PATH, 'w') as f:
            self.names = (set(self.names) | set(self.onames)) - set(self.delnames)
            print('\n'.join(self.names), file = f) 

        self.wal.reset()



    def startup(self) -> None:
        with open(LOG_PATH,'r') as f:
            lines = [i.rstrip('\n') for i in f.readlines()]
            databases = set()
            for i in lines:
                if len(i.split()) == 1:
                    databases.add(i)
            #values = [tuple(i.rstrip('\n').split()) for i in f.readlines()]
            #fixed = [x[0] for x in sorted(list(filter(lambda i : len(i) == 1, set(values))))]
        with open(LIST_PATH, 'a') as f:
            if databases:
                print('\n'.join(databases), file = f) 

        data = {"current_user": None, "current_database": None}

        with open(f'{env.STORAGE_PATH}/state.json', 'w') as f:
            json.dump(data, f, indent=2)
