from socket import *
import asyncio 
import jwt 

from server import env 
import server.database.cluster as cluster 
from server import compact 
from server import statehandler


async def write_message(writer: asyncio.StreamWriter, message: str):
    writer.write(message)
    await writer.drain() 



async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

    init = await reader.read(1024)
    # do stuff here 
    token = init.decode()

    #payload = jwt.decode(token, env.SECRET_KEY, algorithms=['HS256'])
    #username = payload["username"]


    stores = cluster.Cluster(token)

    await write_message(writer, f"\nWelcome to Nano, {stores.username}!\nIf you have any doubts, type help\n".encode())
    print(f"user {stores.username} logged in :)")


    try:
        while True: 
            
            command = await reader.read(1024)
            command = command.decode()
            comlist = command.split()

            if not command:
                #stores.shutdown()
                raise BrokenPipeError()
            

            can = stores.authorize(comlist[0])

            
            if not can:
                print(can, stores.names)
                message = "ERROR. Permission Denied".encode() 


            elif comlist[0] in ('exit', ''):
                stores.shutdown()
                message = 'OK. Exiting Nano............\n'.encode()


            
            elif comlist[0] == 'SHARE':
                message = stores.share(comlist[1], comlist[2]).encode()




            elif comlist[0] == 'LIST':
                message = stores.list().encode()
                #print("encoded the list message", message.decode())



            elif comlist[0] == 'SELECT':
                if len(comlist) != 2:
                    message = f"ERROR. SELECT expected 1 argument (database) but got {len(comlist)}".encode()
                else:
                    message = stores.select(comlist[1]).encode()          


            elif comlist[0] == 'CREATE':
                if len(comlist) != 2:
                    message = f"ERROR. CREATE expected 1 argument (database_name) but got {len(comlist)}".encode()
                else:
                    message = stores.create(comlist[1]).encode()
                

            elif comlist[0] == 'DROP':

                if len(comlist) != 2:
                    message = f"ERROR. CREATE expected 1 argument (database_name) but got {len(comlist)}".encode()

                else:

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
                    
                    if len(comlist) not in (1,2):
                        message = f"GET expected 1 or 2 arguments but received {len(comlist)}".encode()
                    elif len(comlist) == 1:
                        message = "feature yet to be implemented".encode() 
                    else:
                        message = stores.current.get(comlist[1]).encode()



                elif comlist[0] == 'SET':
                    if len(comlist) != 3:
                        message = f"SET expected 2 arguments (key,value) but received {len(comlist)}".encode()
                    else:
                        message = stores.current.set(comlist[1], comlist[2]).encode()
                    


                elif comlist[0] == 'DELETE':
                    if len(comlist) != 2:
                        message = f"DELETE expected 1 argument (key) but received {len(comlist)}".encode()
                    else:
                        message = stores.current.delete(comlist[1]).encode()

                else:   
                    message = f"Invalid command.\nType `help` to check list of valid commands"
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
    statehandler.initialize()
    asyncio.run(main())