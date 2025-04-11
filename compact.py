import os 
import env 

def merge(path, file_1, file_2) -> None:
    f = open(os.path.join(path, file_1), 'r+')
    g = open(os.path.join(path,file_2), 'r+')

    a = []; u = [i.rstrip('\n').split() for i in f.readlines()]; v = [i.rstrip('\n').split() for i in g.readlines()]

    x = 0; y = 0

    while x < len(u) and y < len(v):

        if u[x][0] < v[y][0]:
            a.append(f"{u[x][0]} {u[x][1]}")
            x += 1 
        
        elif u[x][0] > v[y][0]:
            a.append(f"{v[y][0]} {v[y][1]}")
            y += 1 

        if u[x][0] == v[y][0]:
            a.append(f"{u[x][0]} {v[y][1]}")
            x += 1 
            y += 1 
    

    print('\n'.join(a), file=f)     

    f.close()
    g.close()


def compact() -> None:
    while True: 
        for name in os.listdir('./storage'):
            path = os.path.join('./storage', name)
            if os.path.isdir(path):
                s = list(filter(lambda x : 'sstable_datablock' in x, os.listdir(path)))
                if len(s) >= 2 and os.path.getsize(os.path.join(path,s[-1])) and os.path.getsize(os.path.join(path,s[-2])): 
                    merge(path, s[-2], s[-1])
                    corresponding_metablock_index = s[-1].split()[-1]
                    corresponding_metablock = 'sstable_metablock_' + corresponding_metablock_index
                    os.remove(os.path.join(path,s[-1]))
                    os.remove(os.path.join(path,corresponding_metablock))


compact()