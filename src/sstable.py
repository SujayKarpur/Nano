from typing import List, Tuple 
import linecache
import asyncio 

from src.redblacktree import RedBlackTree, TraversalType
from src.bloomfilter import BloomFilter 
from src.wal import WAL 
from src.memtable import Memtable

from env import PATH, FLUSH_SIZE



"""class MetaBlock:

    def __init__(self, name: str, count: int, data: Memtable) -> None:
        self.data = data 
        self.name = name 
        self.count = count 
        self.file_name = f'{PATH}/storage/{name}/sstable_metablock_{count}' 

        bf = BloomFilter()

        ol = data.ordered_list()
        min_key = ol[0]; max_key = ol[-1]

        for node in ol:
            bf.insert(node.key)


        with open(self.file_name, 'w') as f:
            print(bf, file=f)
            print(min_key, max_key, file=f)
            print(data.number_of_elements, file=f)




    def find(self, key: str) -> Tuple[bool,str]:
        
        with open(self.file_name, 'r') as f:
            contents = [i.rstrip('\n') for i in f.readlines()]
            filter_string = contents[0]
            bf = BloomFilter(filter_string)
            if key not in bf:
                return (False, '')
            min_key, max_key = contents[1].split()
            if key < min_key or key > max_key:
                return False 
            n = int(contents[2])
            return #search in the corresponding data file """



class SSTable:

    def __init__(self, name: str) -> None:
        self.number_of_blocks = 0  
        self.name = name 

    
    def meta_block_write(self, data: Memtable) -> None:
        new_file_name = f'{PATH}/storage/{self.name}/sstable_metablock_{self.number_of_blocks}' 

        bf = BloomFilter()

        ol = data.ordered_list()
        min_key = ol[0]; max_key = ol[-1]

        for node in ol:
            bf.insert(node.key)

        with open(new_file_name, 'w') as f:
            print(bf, file=f)
            print(min_key, max_key, file=f)
            print(data.number_of_elements, file=f) 



    def data_block_write(self, data: Memtable) -> None:

        new_file_name = f'{PATH}/storage/{self.name}/sstable_datablock_{self.number_of_blocks}' 

        with open(new_file_name, 'w') as f:
            for node in data.ordered_list():
                print(node.key, node.value, file = f) 



    def write(self, data: Memtable) -> None:
        self.meta_block_write(data)
        self.data_block_write(data)
        self.number_of_blocks += 1 
    

    def find_in_data_block(self, key: str, n: int) -> Tuple[bool,str]:
        #perform a binary search 
        low = 1; high = n

        while low <= high: 

            mid = (low+high)//2 
            mid_line = linecache.getline(mid).rstrip('\n').split()
            mid_key = mid_line[0]

            if mid_key == key:
                return (True, mid_line[1])
            elif key > mid_key:
                low = mid+1 
            else:
                high = mid-1 
        
        return (False, '')




    def find_in_meta_block(self, key: str) -> Tuple[bool,str]:
        current_file_name = f'{PATH}/storage/{self.name}/sstable_metablock_{self.current_block}'
        with open(current_file_name, 'r') as f:
            contents = [i.rstrip('\n') for i in f.readlines()]
            filter_string = contents[0]
            bf = BloomFilter(filter_string)
            if key not in bf:
                return (False, '')
            min_key, max_key = contents[1].split()
            if key < min_key or key > max_key:
                return False 
            n = contents[2]
            return (True, n)



    def find_in_block(self, block_number: int, key: str) -> Tuple[bool,str]:
        self.current_block = block_number
        exists, value = self.find_in_meta_block(key)
        if not exists:
            return (False, '')
        else:
            return self.find_in_data_block(key, int(value))


    

    def find(self, key: str) -> Tuple[bool,str]:
        for block_number in range(self.number_of_blocks-1, -1, -1):
            exists, value = self.find_in_block(block_number, key)
            if exists:
                return exists, value 
        return (False, '')  



    def flush(self, ) -> None:
        pass 

    def get(self, key: str) -> None:
        pass 

    