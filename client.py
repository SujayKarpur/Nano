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
    
    user_option = int(input('> '))

    while user_option not in (1,2,3):
        print("That is not a valid option")
        print("Please enter a number between 1 and 3")
        user_option = int(input('> '))

    
    if user_option == 2:
        succ, ret = auth.signup(input('Enter your username: '), input('Enter your password: '))

        if succ:
            print(ret) 
        else:
            while not succ:
                print(ret)
                ans = input("Would you like to try again?\n")
                if ans not in ('y', 'yes'):
                    exit() 
                succ, ret = auth.signup(input('Enter your username: '), input('Enter your password: '))
            else:
                print(ret)
                print("To use Nano, run the client again and login with your new credentials")
                exit()


    
    if user_option == 1:

        username = input('Enter your username:  ')
        password = input('Enter your password:  ')
        token = auth.login(username, password)

        if not token:
            print("ERROR: Invalid username or password")
        else:
            print(f"Logged In successfully :) w token: {token}")


    

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
                writer.close() 
                await writer.wait_closed() 
                break 




if __name__ == '__main__':
    asyncio.run(main())