import os
import uuid
from MySQLdb import Connect
from settings import DATA_TO_LOGIN_TO_DB

conn = Connect(**DATA_TO_LOGIN_TO_DB)

def convert_str(txt):
    return '"' + txt + '"'

def check_session(cookies):
    if not (cookies.get('user')): return False
    user = cookies['user'].value
    session = cookies['session'].value
    conn = Connect(**DATA_TO_LOGIN_TO_DB)
    curs = conn.cursor()
    is_valid = curs.execute('''SELECT NULL FROM sessions
                               WHERE user_id = %s AND session_id = %s AND expire_time >= CURRENT_TIMESTAMP(); 
                        ''' % (user, convert_str(session)))

    if is_valid:
        return True
    else:
        return False


