from MySQLdb import Connect
from settings import DATA_TO_LOGIN_TO_DB

conn = Connect(**DATA_TO_LOGIN_TO_DB)
curs = conn.cursor()

curs.execute('''INSERT INTO authors (first_name, last_name) VALUES ('J.K', 'Rowling');
             ''')
curs.execute('''INSERT INTO books (title, price, description) VALUES ('Harry Potter', 33.96, "Book about Harry Potter'adventures")''')
conn.commit()

