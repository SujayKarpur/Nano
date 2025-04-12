import json 
from typing import Tuple 
import bcrypt 
import jwt 
import time 


import env 

#from env import USER_STORAGE_PATH, SECRET_KEY


USERS_FILE = f'{env.USER_STORAGE_PATH}/users.json'



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

        with open(f'{env.USER_STORAGE_PATH}/{username}.json', 'w') as f:
            json.dump({"default" : 4}, f)


        return (True, "SIGNED UP SUCCESSFULLY!!")




def login(username: str, password: str) -> str:
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f) 

    if username not in users or not bcrypt.checkpw(password.encode(), users[username].encode()):
        return None 
    
    payload = {"username" : username, "exp" : time.time() + 600}
    token = jwt.encode(payload, env.SECRET_KEY)

    return token 



def logout() -> None:
    env.current_user = None 






def authorize(command: str) -> bool:
    if not env.current_user:
        return command in ('exit', '', )

    payload = jwt.decode(env.current_user, env.SECRET_KEY)
    username = payload["username"]

    with open(f'{env.USER_STORAGE_PATH}/{username}.json') as f:
        access = json.load(f) 