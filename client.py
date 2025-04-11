from socket import socket, AF_INET, SOCK_STREAM
import asyncio 

import env 
import cluster 

def help() -> None:
    print("\n\navailable commands:\n")
    print("LIST")
    print("CREATE <database>")
    print("SELECT <database>")
    print("DROP <database>\n")
    print("SET <key> <value>")
    print("GET <key>")
    print("DELETE <key>\n")
    print("help")
    print("exit\n\n")




async def main():
    print("Welcome to Nano!")
    help() 
    reader, writer = await asyncio.open_connection(env.HOST, env.PORT)
    while True: 
        command = input('> ')
        if not command: 
            writer.close()
            await writer.wait_closed()
            cluster.Cluster.cleanup()
            break 
        if command == 'help':
            help()
            continue  
        elif command == 'exit':
            writer.close()
            await writer.wait_closed() 
            break 
        else:
            writer.write(command.encode())
            await writer.drain()
            output = await reader.read(1024)
            print(output.decode())
            if not output:
                break 



if __name__ == '__main__':
    asyncio.run(main())