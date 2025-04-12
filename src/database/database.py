from src.database.lsm import LSMTree


class Database:

    """
    LSM Tree based key-value store 
    """

    def __init__(self, name: str):
        """ Initialize the database with its name """
        self.db = LSMTree(name)
        self.name = name 


    def set(self, key: str, value: str) -> str:
        """ Database[key] = value """
        if self.db.set(key, value):
            return f"OK. set database[{key}] = {value}"
        else:
            return f"ERROR. Key {key} is reserved internally"
        
        #why can insertions fail? if the client tries to insert a key with value = TOMBSTONE, it could lead to errors
        #thus, we reserve that value internally


    def get(self, key: str) -> str:
        """ Database[key] """
        exists, value = self.db.get(key)

        if exists:
            return value 
        else:
            return f"ERROR: No key {key} exists"
        

        
    def delete(self, key: str) -> str:
        """ del Database[key] """
        if self.db.delete(key):
            return f"OK. removed key {key}"
        else:
            return f"ERROR: No key {key} exists"