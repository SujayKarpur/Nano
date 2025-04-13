from typing import List, Set, Dict 
from os import makedirs 
from shutil import rmtree
from bisect import insort, bisect 
import json 
import jwt 
 
from server.database.database import Database
from server.user.user import User 

from server.statehandler import add_current_database, remove_current_database

from server import env





def list_of_databases(LIST_PATH) -> Dict[str, List]:
    with open(LIST_PATH, 'r') as f:
        data = json.load(f)
    return data 





class Cluster:

    """
    Collection of all Nano databases [tracks global and user-local databases]
    """

    def __init__(self, token: str) -> None: 
        """ Initialize the Cluster when the server starts running """

        self.token = token 
        self.username = jwt.decode(token, env.SECRET_KEY, algorithms=['HS256'])["username"] 
        self.user = User(self.username)


        self.STORAGE_PATH = f'{env.STORAGE_PATH}/{self.username}'
        self.META_STORAGE_PATH = f'{self.STORAGE_PATH}/meta'
        self.LIST_PATH = f'{self.META_STORAGE_PATH}/local.json'
        self.LIST2_PATH = f'{self.META_STORAGE_PATH}/shared.json'
        self.LOG_PATH = f'{self.META_STORAGE_PATH}/wal.log'


        self.names: Dict[str,List] = list_of_databases(self.LIST_PATH)
        self.shared_names: Dict[str,List] = list_of_databases(self.LIST2_PATH)
        

        self.current = Database(self.username, "default") 
        add_current_database("default")




    def __contains__(self, name: str) -> bool:
        return name in self.names


    def create(self, name: str) -> str:

        if name in self.names: 
            return f"Void. Database {name} already exists"

        self.names[name] = [4, self.username]

        with open(self.LIST_PATH, 'r') as f:
            dbs = json.load(f) 
        
        dbs[name] = [4, self.username] 

        with open(self.LIST_PATH, 'w') as f:
            dbs = json.dump(dbs, f, indent=2)

        makedirs(f'{env.STORAGE_PATH}/{self.username}/databases/{name}', exist_ok=True)
        return f"OK. Created new database {name}"
    

    def share(self, username: str, permission_level: int) -> str:

        if self.current.name == "default":
            return "ERROR: Can't share the default database"
        
        with open(f'{env.STORAGE_PATH}/users.json', 'r') as f:
            users = json.load(f)

        if username not in users:
            return "ERROR: No such user exists"
        


        with open(f'{env.STORAGE_PATH}/{username}/meta/shared.json', 'r') as f:
            accesses = json.load(f)

        accesses[self.current.name] = [int(permission_level), self.username]

        with open(f'{env.STORAGE_PATH}/{username}/meta/shared.json', 'w') as f:
            json.dump(accesses, f)


        return f"OK. Granted {username} permission level {permission_level} in database {self.current.name}"


    def drop(self, name: str) -> str:

        if name == "default":
            return "ERROR: Can't delete default database"

        if name == self.current.name:
            remove_current_database(name)
            add_current_database("default")
            self.current = Database(self.username, "default")
            return f"OK. Deleted database {name}"

        if name not in self.names:
            return f"ERROR: No database {name} exists"
        

        self.names.pop(name)

        with open(self.LIST_PATH, 'r') as f:
            dbs = json.load(f) 
        
        dbs.pop(name)

        with open(self.LIST_PATH, 'w') as f:
            dbs = json.dump(dbs, f, indent=2)


        with open(f'{env.STORAGE_PATH}/users.json', 'r') as f:
            user_list = json.load(f)

        for u in user_list:
            with open(f'{env.STORAGE_PATH}/{u}/meta/shared.json', 'r') as f:
                dbs = json.load(f) 
            
            if name in dbs:
                dbs.pop(name)
                with open(f'{env.STORAGE_PATH}/{u}/meta/shared.json', 'w') as f:
                    dbs = json.dump(dbs, f, indent=2)

        
        
        rmtree(f'{env.STORAGE_PATH}/{self.username}/databases/{name}', ignore_errors=True)

        return f"OK. Deleted database {name}"
            


    def list(self) -> str:
        return '\n'.join(self.names | self.shared_names)


    def select(self, name: str) -> str:

        if name == self.current.name:
            return f"Void. Already in database {name}"
        
        if name not in (self.names | self.shared_names):
            return f"ERROR: No database {name} exists"
        

        self.current.shutdown()
        remove_current_database(self.current.name)
        
        if name in self.names:
            self.current = Database(self.username, name)
        
        else:
            self.current = Database(self.shared_names[name][1], name)

        add_current_database(name)
        return f"OK. Selected database {name}"
        

    def shutdown(self) -> None:

        if self.current:
            self.current.shutdown()


    def authorize(self, command: str, optional: int = 0) -> bool:
        
        if command in ('help', 'exit'):
            return True 

        if command in ('LIST', 'CREATE', 'SELECT', 'GET'):
            return True 

        if command in ('SET', 'DELETE'):
            
            print(self.names)

            if self.current.name in self.names:
                return True  

            return self.shared_names[self.current.name][0] > 1


        if command in ('DROP', 'SHARE'):
            if self.current.name in self.names:
                return True  

            return self.shared_names[self.current.name][0] > 2