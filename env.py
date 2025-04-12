import os 


HOST = "127.0.0.1"
PORT = 12345
ADDRESS = (HOST, PORT)

#root path of Nano
PATH = os.path.dirname(os.path.abspath('./env.py'))

#memtable size at which we flush the red-black tree into an SSTable on the disk 
FLUSH_SIZE = 1000


#tombstone value: while deleting a key or a database, insert it with this value instead of deleting it 
#cuz SSTables are immutable 
TOMBSTONE = "__<INTERNAL::TOMBSTONE::v1::42bcf61b>__"

#the database that is currently in use. tracked to avoid compacting while it is in use 
current_database = None 

#the user that is currently in use
current_user = None 

#store all common constant paths here:

NANO_ROOT_PATH: str = PATH 
STORAGE_PATH: str = f'{PATH}/storage'
META_STORAGE_PATH: str = f'{PATH}/storage/meta'
DATABASE_STORAGE_PATH: str = f'{STORAGE_PATH}/databases'
USER_STORAGE_PATH: str = f'{STORAGE_PATH}/users'