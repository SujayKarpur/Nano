from socket import *
import asyncio 
import jwt 

from server import env 
import server.database.cluster as cluster 
from server import compact 



async def write_message(writer: asyncio.StreamWriter, message: str):
    writer.write(message)
    await writer.drain() 



async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

    init = await reader.read(1024)
    # do stuff here 
    token = init.decode()

    payload = jwt.decode(token, env.SECRET_KEY, algorithms=['HS256'])
    username = payload["username"]
    await write_message(writer, f"\nWelcome to Nano, {username}!\nIf you have any doubts, type help\n".encode())
    print(f"user {username} logged in :)")

    stores = cluster.Cluster(username)



    try:
        while True: 
            
            command = await reader.read(1024)
            command = command.decode()
            comlist = command.split()

            if not command:
                stores.shutdown()
                raise BrokenPipeError()
            

            can = stores.authorize(command)

            
            if not can:
                message = "ERROR. Permission Denied".encode() 


            elif comlist[0] in ('exit', ''):
                #stores.current.db.shutdown()
                stores.shutdown()
                message = 'OK. Exiting Nano............\n'.encode()
                #print(f"Client {addr} left :(")


            
            elif comlist[0] == 'SHARE':
                message = stores.share(comlist[1], comlist[2]).encode()




            elif comlist[0] == 'LIST':
                print("trynna list shi here")
                message = stores.list().encode()
                print("encoded the list message", message.decode())



            elif comlist[0] == 'SELECT':
                #env.current = stores.current 
                message = stores.select(comlist[1]).encode()          


            elif comlist[0] == 'CREATE':
                message = stores.create(comlist[1]).encode()
                

            elif comlist[0] == 'DROP':

                if comlist[1] == 'default':
                    message = "ERROR: Can't drop the default database".encode()
                
                else:
                    msg = stores.drop(comlist[1])                    
                    message = msg.encode()

            else:
                if stores.current == None:
                    message = "ERROR. No database selected".encode()
                else:
                    pass #stores.current.wal.write(command)


                if comlist[0] == 'GET':
                    message = stores.current.get(comlist[1]).encode()

                elif comlist[0] == 'SET':
                    message = stores.current.set(comlist[1], comlist[2]).encode()

                elif comlist[0] == 'DELETE':
                    message = stores.current.delete(comlist[1]).encode()

                else:   
                    break 
            
            await write_message(writer, message)


    except BrokenPipeError:
        pass 
        #print(f"Client {addr} closed the connection")


    finally:
        writer.close()
        await writer.wait_closed()


async def main():

    asyncio.create_task(compact.compact()) #asynchronously compact SSTables 

    server = await asyncio.start_server(handle_client, env.HOST, env.PORT)
    print("Server is listening")
    async with server:
        await server.serve_forever()


                
 


if __name__ == '__main__':
    #stores = cluster.Cluster()
    #env.current = stores.current
    asyncio.run(main())