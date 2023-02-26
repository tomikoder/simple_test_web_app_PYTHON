from MySQLdb import Connect
from settings import DATA_TO_LOGIN_TO_DB

conn = Connect(**DATA_TO_LOGIN_TO_DB)
curs = conn.cursor()

curs.execute('''CREATE TABLE IF NOT EXISTS books (
                  book_id int NOT NULL AUTO_INCREMENT,
                  title char(50),
                  price DECIMAL(3,2),
                  PRIMARY KEY (book_id)
                );   
             ''')

curs.execute('''CREATE TABLE IF NOT EXISTS authors (
                  author_id int NOT NULL AUTO_INCREMENT,
                  first_name char(50),
                  last_name char(50),
                  PRIMARY KEY (author_id)
                );   
             ''')

curs.execute('''CREATE TABLE IF NOT EXISTS authors_books (
                  book_id int,
                  author_id int,
                  FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE,
                  FOREIGN KEY (author_id) REFERENCES authors (author_id) ON DELETE CASCADE
                );
             ''')

curs.execute('''CREATE TABLE IF NOT EXISTS users (
                  user_id int NOT NULL AUTO_INCREMENT,
                  email char(50),
                  password char(50),
                  is_loged bool default TRUE, 
                  PRIMARY KEY (user_id),
                  UNIQUE (email)
                );
             ''')

curs.execute('''CREATE TABLE IF NOT EXISTS sessions (
                  session_id char (50),
                  user_id int,
                  expire_time timestamp NOT NULL,
                  PRIMARY KEY (session_id),
                  FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                );
             ''')













