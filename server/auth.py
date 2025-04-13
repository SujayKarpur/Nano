from server.user.user import User 

from server.statehandler import get_current_db_name




def authorize(user: User, command: str) -> bool:

    print('check the current user ', user)

    current_db = get_current_db_name()

    if command in ('exit', '', 'LOGIN'):
        return True 
    
    if command in ('LIST', 'LOGOUT', 'SELECT', 'CREATE'):
        return user != None 
    
    if command in ('GET'):
        return current_db in user.read()
    
    if command in ('SET', 'DELETE'):
        return current_db in user.write()

    if command in ('SHARE', 'DROP', ):
        return current_db in user.modify()

    if command in ():
        return current_db in user.own()
