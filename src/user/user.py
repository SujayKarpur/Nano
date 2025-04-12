from typing import List 
import jwt 
import json 

import env  


class User:
    
    def __init__(self, token: str) -> None:
        payload = jwt.decode(token, env.SECRET_KEY)
        self.username = payload["username"] 

        with open(f'{env.USER_STORAGE_PATH}/{self.username}.json', 'r') as f:
            self.accesses = json.load(f)
        


     
    def read(self, ) -> List[str]:
        pass 

    def write(self, ) -> List[str]:
        pass 

    def modify(self, ) -> List[str]:
        pass 

    def own(self, ) -> List[str]:
        pass 
    

    def shutdown(self) -> None:
        pass 