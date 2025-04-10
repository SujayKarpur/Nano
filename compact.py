import os 
import asyncio 

import env 

def merge(path, file_1, file_2) -> None:
    f = open(os.path.join(path, file_1), 'r+')
    g = open(os.path.join(path,file_2), 'r+')

    a = []; u = sorted(dict([i.rstrip('\n').split() for i in f.readlines()]).items()); v = sorted(dict([i.rstrip('\n').split() for i in g.readlines()]).items())

    x = 0; y = 0

    while x < len(u) and y < len(v):

        if u[x][0] < v[y][0]:
            a.append(f"{u[x][0]} {u[x][1]}")
            x += 1 
        
        elif u[x][0] > v[y][0]:
            a.append(f"{v[y][0]} {v[y][1]}")
            y += 1 

        if u[x][0] == v[y][0]:
            if v[y][1] not in a:
                a.append(f"{u[x][0]} {v[y][1]}")
            x += 1 
            y += 1 
    

    print('\n'.join(a), file=f)     

    f.close()
    g.close()


async def compact() -> None:
    while True: 
        for name in os.listdir('./storage'):
            print(name)
            path = os.path.join('./storage', name)
            if os.path.isdir(path) and name != env.current:
                s = list(filter(lambda x : 'sstable_datablock' in x, os.listdir(path)))
                if len(s) > 0:
                    for indexo in range(len(s)):
                        while not os.path.getsize(os.path.join(path,s[indexo])):
                            corresponding_metablock_index = s[indexo].split('_')[-1]
                            corresponding_metablock = 'sstable_metablock_' + corresponding_metablock_index
                            os.remove(os.path.join(path,corresponding_metablock))
                            os.remove(os.path.join(path,s[indexo]))
                            s.pop(indexo) 
                            break 
                if len(s) >= 2 and os.path.getsize(os.path.join(path,s[-1])) and os.path.getsize(os.path.join(path,s[-2])): 
                    merge(path, s[-2], s[-1])
                    corresponding_metablock_index = s[-1].split('_')[-1]
                    corresponding_metablock = 'sstable_metablock_' + corresponding_metablock_index
                    os.remove(os.path.join(path,s[-1]))
                    os.remove(os.path.join(path,corresponding_metablock))


        if __name__ != '__main__':
            await asyncio.sleep(5)


if __name__ == '__main__':
    env.current = None 
    asyncio.run(compact())