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
    is_valid = curs.execute('''SELECT NULL FROM sessions AS s INNER JOIN users AS u ON s.user_id = u.user_id
                               WHERE s.user_id = %s AND s.session_id = %s AND s.expire_time >= CURRENT_TIMESTAMP() AND u.is_loged = TRUE; 
                        ''' % (user, convert_str(session)))

    if is_valid:
        curs.execute('''UPDATE sessions
                        SET expire_time = DATE_ADD(now() , INTERVAL 10 MINUTE)
                        WHERE user_id = %s; 
                     ''' % (user))
        conn.commit()
        return True
    else:
        return False

def translate_to_sql(form):
    sql = []
    sql.append(form['title'].value)
    if form['price'].value == '':
        sql.append(0.0)
    else:
        sql.append(float(form['price'].value))
    sql.append(form['description'].value)
    sql = tuple(sql)
    return str(sql)



