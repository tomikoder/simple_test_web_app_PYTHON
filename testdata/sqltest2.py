from MySQLdb import Connect
import uuid
from helpfunctions import convert_str

conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()


add = (1, 2, 3)
for id in remove:
  curs.execute('''DELETE FROM authors_books WHERE author_id IN %s;
                 ''' % (str(remove)))




