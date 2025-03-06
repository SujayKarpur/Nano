from socket import socket, AF_INET, SOCK_STREAM

import env 

def help() -> None:
    print("\n\navailable commands:")
    print("SET <name> <value>")
    print("GET <name>")
    print("DELETE <name>")
    print("help")
    print("exit\n\n")




def main():
    print("Welcome to Nano!")
    help() 
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(env.ADDRESS)
        while True: 
            command = input('> ')
            if not command: 
                s.close()
                break 
            if command == 'help':
                help()
                continue  
            elif command == 'exit':
                s.close()  
                break 
            else:
                s.send(command.encode())
                output = s.recv(1024).decode()
                print(output)



if __name__ == '__main__':
    main()