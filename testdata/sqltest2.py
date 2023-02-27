from MySQLdb import Connect
import uuid
from helpfunctions import convert_str

conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()
mail = '"tom@wp.pl"'
password = "'lol'"
session = str(uuid.uuid1())

test = curs.execute('''INSERT INTO sessions (session_id, user_id, expire_time)
                                    VALUES  (%s, %s, CURRENT_TIMESTAMP() + 10000);
                    ''' % (convert_str(session), 1))

for row in curs.fetchall():
  print(row)






