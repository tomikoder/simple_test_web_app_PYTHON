from MySQLdb import Connect

conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()
curs.execute('SELECT EXISTS(SELECT NULL FROM persons WHERE id = 1);')

for row in curs.fetchall():
  print(row)
