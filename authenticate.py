import json 
import jwt 
import bcrypt 
import os 
from typing import Tuple 

from server import env


USERS_FILE = f'{env.STORAGE_PATH}/users.json'


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
            json.dump({"default" + username : 4}, f)

        os.makedirs(f'{env.DATABASE_STORAGE_PATH}/{"default" + username}', exist_ok = True)

        return (True, "SIGNED UP SUCCESSFULLY!!")




def login(username: str, password: str) -> str:
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f) 

    if username not in users:
        return "ERROR: Invalid username" 
    
    if not bcrypt.checkpw(password.encode(), users[username].encode()):
        return "ERROR: Incorrect password"
    
    payload = {"username" : username}
    token = jwt.encode(payload, env.SECRET_KEY, algorithm='HS256')


    return f"!{token}"



def logout() -> str:
    return "OK. Logged Out successfully"