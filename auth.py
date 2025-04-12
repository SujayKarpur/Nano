import json 
from typing import Tuple 
import bcrypt 
import jwt 
import time 


from env import USER_STORAGE_PATH, SECRET_KEY


USERS_FILE = f'{USER_STORAGE_PATH}/users.json'



def signup(username: str, password: str) -> Tuple[bool, str]:
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f) 

    if username in users:
        return (False, "ERROR: That username already exists")
    
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        users[username] = hashed_password

        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)

        with open(f'{USER_STORAGE_PATH}/{username}.json', 'w') as f:
            json.dump({"default" : 4}, f)


        return (True, "SIGNED UP SUCCESSFULLY!!")




def login(username: str, password: str) -> str:
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f) 

    if username not in users or not bcrypt.checkpw(password, users[username]):
        return None 
    
    payload = {"username" : username, "exp" : time.time() + 600}
    token = jwt.encode(payload, SECRET_KEY)

    return token 



def logout() -> None:
    pass 