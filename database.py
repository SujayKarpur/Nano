from redblacktree import RedBlackTree


class Database:

    def __init__(self):
        self.db = RedBlackTree()

    def __repr__(self) -> str:
        return self.db.__repr__()

    def set(self, key: str, value: str) -> str:
        self.db.insert(key, value)
        return f"OK. set database[{key}] = {value}"

    def get(self, key: str) -> str:
        if key in self.db:
            return self.db[key]
        else:
            return f"ERROR: No key {key} exists"
        
    def delete(self, key: str) -> str:
        if key in self.db:
            self.db.delete(key)
            return f"OK. removed key {key}"
        else:
            return f"ERROR: No key {key} exists"
