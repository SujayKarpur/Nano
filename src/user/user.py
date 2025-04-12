from typing import List 

import env  


class User:
    
    def __init__(self, username: str) -> None:
        self.username = username 

     
    def read_access(self, ) -> List[str]:
        pass 