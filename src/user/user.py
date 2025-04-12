from typing import List 
import jwt 
import json 

import env  


class User:
    
    def __init__(self, token: str) -> None:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=['HS256'])
        self.username = payload["username"] 

        with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'r') as f:
            self.accesses = json.load(f)
        


     
    def read(self, ) -> List[str]:
        with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'r') as f:
            accesses = json.load(f) 
        
        return list(filter(lambda i : accesses[i] > 0, accesses))


    def write(self, ) -> List[str]:
        with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'r') as f:
            accesses = json.load(f) 
        
        return list(filter(lambda i : accesses[i] > 1, accesses))
    


    def modify(self, ) -> List[str]:
        with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'r') as f:
            accesses = json.load(f) 
        
        return list(filter(lambda i : accesses[i] > 1, accesses))
    


    def own(self, ) -> List[str]:
        with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'r') as f:
            accesses = json.load(f) 
        
        return list(filter(lambda i : accesses[i] > 1, accesses))
    


    def shutdown(self) -> None:
        with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'r') as f:
            accesses = json.load(f) 
        
        return list(filter(lambda i : accesses[i] > 1, accesses))