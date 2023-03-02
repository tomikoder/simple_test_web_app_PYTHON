from jinja2 import Environment, FileSystemLoader
import http.cookies, os, cgi
from settings import DATA_TO_LOGIN_TO_DB, PROJECT_DIR, YOUR_DOMAIN
from MySQLdb import Connect
from helpfunctions import check_session
import string

environment = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, 'templates')))

cookstr = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cookstr)

form = cgi.FieldStorage()

is_loged = check_session(cookies)


if not (is_loged):

    link_to_redirect = YOUR_DOMAIN + 'login.py'
    print('Refresh: 0; %s' % link_to_redirect)
elif os.environ['REQUEST_METHOD'] == 'POST':
    form = cgi.FieldStorage()
    template = environment.get_template("test.html")
    print(cookies)
    print(template.render(val=form))


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
    does_row_exist = curs.execute('''SELECT GROUP_CONCAT(CAST(a.author_id AS CHAR), ' ') AS authors_id, GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name), ' ') AS authors, b.* FROM authors AS a INNER JOIN authors_books AS ab ON a.author_id = ab.author_id
                                                              INNER JOIN books AS b ON b.book_id = ab.book_id
                                                              GROUP BY b.book_id;    
                                  ''')
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
        authors_id = authors_id.split(',')
        for indx in range(len(authors_id)):
            authors_id[indx] = int(authors_id[indx])
        authors_id = str(tuple(authors_id))

        all_authors = curs.execute('''SELECT author_id, CONCAT(first_name, ' ', last_name) AS full_name, author_id IN %s AS author_belong FROM authors
                                      ''' % (authors_id))

        all_authors_columns = [i[0] for i in curs.description]
        all_authors = curs.fetchall()
        all_authors = [dict(zip(all_authors_columns, row)) for row in all_authors]
        authors = book['authors']
        authors = authors.split(',')
        authors = dict(zip(authors, authors_id))
        print("Content-type: text/html")
        print(cookies)
        print(template.render(book=book, all_authors=all_authors))








