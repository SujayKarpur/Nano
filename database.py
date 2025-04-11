from src.memtable import Memtable


class Database:

    count: int = 0

    def __init__(self, name: str):
        self.db = Memtable()
        self.name = name 
        self.id = Database.count 
        Database.count += 1 


    def __repr__(self) -> str:
        return self.db.__repr__()

    def set(self, key: str, value: str) -> str:
        if self.db.set(key, value):
            return f"OK. set database[{key}] = {value}"
        else:
            return f"ERROR. Key {key} is reserved internally"

    def get(self, key: str) -> str:
        exists, value = self.db.get(key)

        if exists:
            return value 
        else:
            return f"ERROR: No key {key} exists"
        
        
    def delete(self, key: str) -> str:
        if self.db.delete(key):
            return f"OK. removed key {key}"
        else:
            return f"ERROR: No key {key} exists"