from jinja2 import Environment, FileSystemLoader
import http.cookies, os, cgi
from settings import DATA_TO_LOGIN_TO_DB, PROJECT_DIR, YOUR_DOMAIN
from MySQLdb import Connect
from helpfunctions import check_session

environment = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, 'templates')))

cookstr = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cookstr)

is_loged = check_session(cookies)


if not (is_loged):

    link_to_redirect = YOUR_DOMAIN + 'login.py'
    print('Refresh: 0; %s' % link_to_redirect)
else:

    environment = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, 'templates')))
    template = environment.get_template("menu.html")
    conn = Connect(**DATA_TO_LOGIN_TO_DB)
    curs = conn.cursor()
    curs.execute('''SELECT email FROM users WHERE user_id = %s;''' % (cookies['user'].value))
    email =  curs.fetchone()[0]
    curs.execute('''SELECT GROUP_CONCAT(CAST(a.author_id AS CHAR), ' ') AS authors_id, GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name), ' ') AS authors, b.* FROM authors AS a INNER JOIN authors_books AS ab ON a.author_id = ab.author_id
                                                              INNER JOIN books AS b ON b.book_id = ab.book_id
                                                              GROUP BY b.book_id;    
                 ''')
    columns_names = [i[0] for i in curs.description]
    books = curs.fetchall()
    books = [dict(zip(columns_names, row)) for row in books]
    for row in books:
        row_to_process = row['authors'].split(',')
        row['authors'] = row_to_process
        for idx in range(len(row_to_process)):
            row_to_process[idx] = row_to_process[idx].rstrip()
        row_to_process = ', '.join(row_to_process)
        row['authors'] = row_to_process
    print(cookies)
    print(template.render(email=email, books=books))
