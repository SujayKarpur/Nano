from typing import Any, Optional, Tuple, List 

from env import PATH 


def list_of_databases() -> List[str]:
    with open(f'{PATH}/storage/meta/list.txt', 'r') as f:
        names = [i.rstrip('\n') for i in f.readlines()]
    return names 