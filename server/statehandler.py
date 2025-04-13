import json 
import jwt 


from server.env import STORAGE_PATH, SECRET_KEY



#designing state json
#in progress
#current idea : currently logged in user ka token + db name??

STATE_FILE = f'{STORAGE_PATH}/state.json'






def get_current_db_name() -> str:
    with open(STATE_FILE, 'r') as f:
        data = json.load(f) 
    return data["current_database"]


def set_current_db_name(name: str) -> None:
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
    
    data["current_database"] = name 

    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)