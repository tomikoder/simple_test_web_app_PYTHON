from jinja2 import Environment, FileSystemLoader
import http.cookies, os, cgi
from settings import DATA_TO_LOGIN_TO_DB, PROJECT_DIR, YOUR_DOMAIN
from MySQLdb import Connect
from helpfunctions import check_session
import string
from helpfunctions import convert_str, translate_to_sql
from form_validator import add_book_validate_form_data
import sys

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
    errors = add_book_validate_form_data(form)
    if (errors):
        template = environment.get_template("update_db_error.html")
        link_to_redirect = YOUR_DOMAIN + 'add_book.py'

        print('Refresh: 0; %s' % link_to_redirect)
        print("Content-type: text/html")
        print(cookies)
        print(template.render(errors=errors))
    else:
        curs.execute('''INSERT INTO books (title, price, description) VALUES %s;
                     ''' % (translate_to_sql(form)))
        conn.commit()

        curs.execute('''SELECT book_id from books
                        WHERE title = %s;
                     ''' % (convert_str(form['title'].value)))

        book_id = curs.fetchone()[0]

        if not 'authors' in form:
            authors_id = set()
        elif isinstance(form['authors'], list):
            authors_id = set(int(a_id.value) for a_id in form['authors'])
        else:
            authors_id = set()
            authors_id.add(int(form['authors'].value))

        for a in authors_id:
            curs.execute('''INSERT INTO authors_books (author_id, book_id) VALUES (%s, %s);
                         ''' % (a, book_id))
        conn.commit()

        actions = ['Book was added to db.']
        template = environment.get_template("update_db_success.html")

        link_to_redirect = YOUR_DOMAIN + 'menu.py'
        print(cookies)
        print('Refresh: 5; %s' % link_to_redirect)
        print(template.render(actions=actions))







else:

    template = environment.get_template("add_book.html")
    conn = Connect(**DATA_TO_LOGIN_TO_DB)
    curs = conn.cursor()

    curs.execute('''SELECT author_id, CONCAT(first_name, ' ', last_name) AS full_name
                                 FROM authors;
                              ''')

    all_authors_columns = [i[0] for i in curs.description]
    all_authors = curs.fetchall()
    all_authors = [dict(zip(all_authors_columns, row)) for row in all_authors]
    print(cookies)
    print(template.render(all_authors=all_authors))







