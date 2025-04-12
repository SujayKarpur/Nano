import os 
import secrets 


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
#current_database = None 

#the user that is currently logged in
#current_user = None 

#store all common constant paths here:

NANO_ROOT_PATH: str = PATH 
STORAGE_PATH: str = f'{PATH}/storage'
META_STORAGE_PATH: str = f'{PATH}/storage/meta'
DATABASE_STORAGE_PATH: str = f'{STORAGE_PATH}/databases'
META_DATABASE_STORAGE_PATH: str = f'{DATABASE_STORAGE_PATH}/meta'
USER_STORAGE_PATH: str = f'{STORAGE_PATH}/users'
META_USER_STORAGE_PATH = f'{USER_STORAGE_PATH}/meta'


CURRENT_USER = f'{STORAGE_PATH}/cu_token.txt'
CURRENT_DATABASE = f'{STORAGE_PATH}/cu_db.txt'




# secret key for jwt 
SECRET_KEY = 'fba3ec6d931431cb05ea064d0569a513cb04a9a4595319dfc188bba7a07b4d42'
