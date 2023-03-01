from MySQLdb import Connect
from helpfunctions import convert_str



conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()

curs.execute('''SELECT author_id, CONCAT(first_name, ' ', last_name) AS full_name FROM authors;    
             ''')

for row in curs.fetchall():
  print(row)


