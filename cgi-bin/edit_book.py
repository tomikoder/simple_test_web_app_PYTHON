from jinja2 import Environment, FileSystemLoader
import http.cookies, os, cgi
from settings import DATA_TO_LOGIN_TO_DB, PROJECT_DIR, YOUR_DOMAIN
from MySQLdb import Connect
from helpfunctions import check_session
import string
from helpfunctions import convert_str

environment = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, 'templates')))

cookstr = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cookstr)

form = cgi.FieldStorage()

is_loged = check_session(cookies)


if not (is_loged):

    link_to_redirect = YOUR_DOMAIN + 'login.py'
    print('Refresh: 0; %s' % link_to_redirect)
elif os.environ['REQUEST_METHOD'] == 'POST':
    conn = Connect(**DATA_TO_LOGIN_TO_DB)
    curs = conn.cursor()


    template = environment.get_template("update_db_success.html")
    if isinstance(form['authors'], list):
        authors_id =  set(int(a_id.value) for a_id in form['authors'])
    else:
        authors_id = set()
        authors_id.add(form['authors'].value)
    curs.execute('''UPDATE books SET title = %s,
                                     description = %s,
                                     price = %s    
                                 WHERE book_id = %s;
                 ''' % (convert_str(form['title'].value), convert_str(form['description'].value), form['price'].value, form['book_id'].value))

    curs.execute('''SELECT a.author_id FROM authors AS a INNER JOIN authors_books AS ab ON a.author_id = ab.author_id
                                                              INNER JOIN books AS b ON b.book_id = ab.book_id
                                                              WHERE b.book_id = %s 
                                  ''' % (form['book_id'].value))
    authors_id2 = curs.fetchall()
    authors_id2 = set(a[0] for a in authors_id2)

    to_remove = authors_id2 - authors_id
    to_add = authors_id - authors_id2

    if not (authors_id == authors_id2):
        for a in to_add:
            curs.execute('''INSERT INTO authors_books (author_id, book_id) VALUES (%s, %s); 
                         ''' % (a, form['book_id'].value))
        for a in to_remove:
            curs.execute('''DELETE FROM authors_books WHERE author_id = %s; 
                         ''' % (a))
    conn.commit()
    link_to_redirect = YOUR_DOMAIN + 'edit_book.py'
    print(cookies)
    print('Refresh: 5; %s' % link_to_redirect)
    print(template.render())


elif 'book_id' not in form:
    template = environment.get_template("update_db_error.html")
    errors = ['No data required to perform operation.']
    link_to_redirect = YOUR_DOMAIN + 'add_author.py'
    print(cookies)
    print('Refresh: 5; %s' % link_to_redirect)
    print(template.render(errors=errors))

else:
    conn = Connect(**DATA_TO_LOGIN_TO_DB)
    curs = conn.cursor()
    does_row_exist = curs.execute('''SELECT GROUP_CONCAT(CAST(a.author_id AS CHAR), ' ') AS authors_id, GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name), ' ') AS authors, b.* FROM books AS b LEFT JOIN authors_books AS ab ON b.book_id = ab.book_id
                                                                            LEFT JOIN authors AS a  ON a.author_id = ab.author_id
                                     WHERE b.book_id = %s                                            
                                     GROUP BY b.book_id;    
                                  ''' % (form['book_id'].value))
    if not does_row_exist:
        template = environment.get_template("update_db_error.html")
        errors = ['Row does not exists']
        link_to_redirect = YOUR_DOMAIN + 'menu.py'
        print(cookies)
        print('Refresh: 5; %s' % link_to_redirect)
        print(template.render(errors=errors))
    else:
        template = environment.get_template("edit_book.html")
        columns_names = [i[0] for i in curs.description]
        books = curs.fetchall()
        books = [dict(zip(columns_names, row)) for row in books]
        book = books[0]

        authors_id = book['authors_id']

        if (authors_id != None):
            authors_id = authors_id.split(',')
            if (len(authors_id) > 1):
                for indx in range(len(authors_id)):
                    authors_id[indx] = int(authors_id[indx])
                authors_id = str(tuple(authors_id))
                sql_string = 'author_id IN %s' % authors_id
            else:
                authors_id = '(%s)' % authors_id[0]
                sql_string = 'author_id IN %s' % (authors_id)
        else:
            sql_string = 'FALSE'


        all_authors = curs.execute('''SELECT author_id, CONCAT(first_name, ' ', last_name) AS full_name, %s AS author_belong FROM authors
                                    ''' % (sql_string))
        all_authors_columns = [i[0] for i in curs.description]
        all_authors = curs.fetchall()
        all_authors = [dict(zip(all_authors_columns, row)) for row in all_authors]
        print("Content-type: text/html")
        print(cookies)
        print(template.render(book=book, all_authors=all_authors))









