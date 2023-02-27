from MySQLdb import Connect

conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()
mail = '"tom@wp.pl"'
password = "'lol'"
session = '"dfdfsdfs23asd"'

test = curs.execute('''INSERT INTO sessions (session_id, user_id, expire_time)
                                    VALUES  (%s, 1, CURRENT_TIMESTAMP() + 10000);
                    ''' % (session))


test = curs.execute(''' UPDATE sessions
                        SET session_id = CURRENT_TIMESTAMP() + 10000
                        WHERE user_id = 1; 
                    ''')

test = curs.execute('''SELECT u.*, s.* FROM
                            users AS u INNER JOIN sessions AS s ON u.user_id = s.user_id;
                    ''')

for row in curs.fetchall():
  print(row)

conn.commit()





