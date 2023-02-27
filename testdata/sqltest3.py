from MySQLdb import Connect
from helpfunctions import convert_str



conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()

user = 1
session = curs.execute('''SELECT NULL FROM sessions
                          WHERE user_id = %s AND expire_time <= CURRENT_TIMESTAMP()     
                       ''')
is_valid = curs.execute('''SELECT NULL FROM sessions
                           WHERE user_id = %s AND session_id = %s AND expire_time <= CURRENT_TIMESTAMP(); 
                    ''' % (user, convert_str(session)))
