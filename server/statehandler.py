import json 
from typing import List, Set 


from server.env import PATH 



#designing state json
#in progress
#current idea : currently logged in user ka token + db name??

STATE_FILE = f'{PATH}/server/state.json'



def initialize() -> None:
    s = {"current_databases" : None}
    with open(STATE_FILE, 'w') as f:
        json.dump(s,f,indent=2)




def get_current_databases() -> Set[str]:
    with open(STATE_FILE, 'r') as f:
        data = json.load(f) 
    return set(data["current_databases"])



def add_current_database(name: str) -> None:
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
    
    data["current_database"].append(name)

    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def remove_current_database(name: str) -> None:
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
    
    data["current_database"].remove(name)

    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)