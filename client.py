from socket import socket, AF_INET, SOCK_STREAM
import asyncio 

import env 
import auth 
from src.user.user import User 



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




def startup() -> None:
    auth.logout()
    print("\n\nWelcome to Nano!\n")
    print("Nano is a lightweight, secure key value store with concurrency control")
    print('\n\n')
    print('1 - LOGIN (if you already have a Nano account)')
    print('2 - SIGN UP (to create a new Nano account!)')
    print('3 - TEMP (to continue incognito - changes you made will not be saved!)') 
    print('\n\n')




async def main():


    startup()
    reader, writer = await asyncio.open_connection(env.HOST, env.PORT)


    while True: 
        command = input('> ')
        if command == 'help':
            help()
            continue  

        if command in ('LOGIN', 'SIGNUP'):
            username = input('\nEnter your username: ')
            password = input('Enter your password: ')
            print()
            command = command + ' ' + username + ' ' + password 

        writer.write(command.encode())
        await writer.drain()
        output = await reader.read(1024)
        print(output.decode())
        if not output or not command or command == 'exit':
            writer.close() 
            await writer.wait_closed() 
            break 




if __name__ == '__main__':
    asyncio.run(main())