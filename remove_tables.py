from MySQLdb import Connect
from settings import DATA_TO_LOGIN_TO_DB

conn = Connect(**DATA_TO_LOGIN_TO_DB)
curs = conn.cursor()

curs.execute('''DROP TABLE IF EXISTS authors_books;
                DROP TABLE IF EXISTS sessions;
                DROP TABLE IF EXISTS books;
                DROP TABLE IF EXISTS users;
                DROP TABLE IF EXISTS authors;
             ''')
