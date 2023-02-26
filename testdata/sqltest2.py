from MySQLdb import Connect

conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()
curs.execute('''
                SELECT emai FROM users WHERE emai = 'tom@wp.pl';
            ''')

for row in curs.fetchall():
  print(row[0])
