from MySQLdb import Connect
from helpfunctions import convert_str
from settings import DATA_TO_LOGIN_TO_DB



conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()

f_n = 'Adolf'
l_n = 'Hitler'
conn = Connect(**DATA_TO_LOGIN_TO_DB)
curs = conn.cursor()

does_row_exist = curs.execute('''SELECT GROUP_CONCAT(CAST(a.author_id AS CHAR), ' ') AS authors_id, GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name), ' ') AS authors, b.* FROM books AS b LEFT JOIN authors_books AS ab ON b.book_id = ab.book_id
                                                                        LEFT JOIN authors AS a  ON a.author_id = ab.author_id     
                                 GROUP BY b.book_id;    
                              ''')

d = curs.fetchall()
print(d)

