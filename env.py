import os 


HOST = "127.0.0.1"
PORT = 12345
ADDRESS = (HOST, PORT)

PATH = os.path.dirname(os.path.abspath('./env.py'))

FLUSH_SIZE = 1000

TOMBSTONE = "__<INTERNAL::TOMBSTONE::v1::42bcf61b>__"
