import json 
from typing import List, Set 


from server.env import PATH 



#designing state json
#in progress
#current idea : currently logged in user ka token + db name??

STATE_FILE = f'{PATH}/server/state.json'



def initialize() -> None:
    s = {"current_databases" : []}
    with open(STATE_FILE, 'w') as f:
        json.dump(s,f,indent=2)




def get_current_databases() -> Set[str]:
    with open(STATE_FILE, 'r') as f:
        data = json.load(f) 
    
    if not data:
        return set()
    
    return set(data["current_databases"])



def add_current_database(name: str) -> None:
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
    
    try:
        data["current_databases"].append(name)
    except:
        data["current_databases"] = [name]

    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def remove_current_database(name: str) -> None:
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
    
    try:
        data["current_databases"].remove(name)
    except:
        pass 

    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)