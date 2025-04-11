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
        if command == 'help':
            help()
            continue  
        else:
            writer.write(command.encode())
            await writer.drain()
            output = await reader.read(1024)
            print(output.decode())
            if not output or not command or command == 'exit':
                break 



if __name__ == '__main__':
    asyncio.run(main())