from MySQLdb import Connect
from helpfunctions import convert_str



conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()

user = 1
is_valid = curs.execute('''SELECT expire_time <= CURRENT_TIMESTAMP() AS test  FROM sessions
                           WHERE user_id = 1; 
                    ''')

print(is_valid)
