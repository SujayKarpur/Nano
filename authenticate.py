import json 
import jwt 
import bcrypt 
import os 
from typing import Tuple 

from server import env


USERS_FILE = f'{env.STORAGE_PATH}/users.json'


def signup(username: str, password: str) -> Tuple[bool, str]:

    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f) 

        if username in users:
            return (False, "ERROR: That username already exists")
    
    except:
        users = dict() 
    
    
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed_password

    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

    with open(f'{env.STORAGE_PATH}/{username}/meta/local.json', 'w') as f:
        json.dump({"default" : 4}, f)

    with open(f'{env.STORAGE_PATH}/{username}/meta/shared.json', 'w') as f:
        json.dump({}, f)

    os.makedirs(f'{env.STORAGE_PATH}/{username}', exist_ok = True)
    os.makedirs(f'{env.STORAGE_PATH}/{username}/databases/default', exist_ok=True)
    os.makedirs(f'{env.STORAGE_PATH}/{username}/meta', exist_ok=True)

    return (True, "SIGNED UP SUCCESSFULLY!!")




def login(username: str, password: str) -> str:
    
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f) 
    except json.JSONDecodeError:
        return 'E'

    if username not in users:
        return "ERROR: Invalid username" 
    
    if not bcrypt.checkpw(password.encode(), users[username].encode()):
        return "ERROR: Incorrect password"
    
    payload = {"username" : username}
    token = jwt.encode(payload, env.SECRET_KEY, algorithm='HS256')


    return f"!{token}"



def logout() -> str:
    return "OK. Logged Out successfully"