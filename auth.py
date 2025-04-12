import json 
from typing import Tuple 
import bcrypt 
import jwt 
import time 

from src.user.user import User 
import env 

from storage.statehandler import get_current_username, get_current_db_name, set_current_user_token

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
            json.dump({"default" + username : 4}, f)


        return (True, "SIGNED UP SUCCESSFULLY!!")




def login(username: str, password: str) -> str:
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f) 

    if username not in users or not bcrypt.checkpw(password.encode(), users[username].encode()):
        return None 
    
    payload = {"username" : username, "exp" : time.time() + 600}
    token = jwt.encode(payload, env.SECRET_KEY, algorithm='HS256')

    set_current_user_token(token)

    return token 



def logout() -> None:
    set_current_user_token(None)






def authorize(user: User, command: str) -> bool:

    print('check the current user ', user)

    current_db = get_current_db_name()

    if not user:
        return command in ('exit', '', )

    if current_db in user.own():
        return True 
    
    if current_db in user.modify():
        return True 
    
    if current_db in user.write():
        return command not in ('SHARE', 'DROP')

    if current_db in user.read():
        return command in ('LIST', '', 'exit', 'GET', 'SELECT', 'LOGOUT')
    
    return command in ('LIST', '', 'exit', 'LOGOUT', 'SELECT')