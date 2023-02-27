from MySQLdb import Connect
from helpfunctions import convert_str
conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()

mail = '"tom@wp.pl"'
password = "'lol'"

user_id = 1

c = curs.execute('''SELECT session_id FROM sessions
                       WHERE user_id = 1;
                    ''')

session = curs.fetchone()[0]

test = curs.execute('''SELECT NULL FROM sessions AS s INNER JOIN users AS u ON s.user_id = u.user_id 
                       WHERE s.user_id = %s AND s.expire_time <= CURRENT_TIMESTAMP() AND s.session_id = %s AND u.is_loged = TRUE;
                    ''' % (user_id, convert_str(session)))
print(test)
