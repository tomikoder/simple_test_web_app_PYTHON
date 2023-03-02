from jinja2 import Environment, FileSystemLoader
import http.cookies, os, cgi
from settings import DATA_TO_LOGIN_TO_DB, PROJECT_DIR, YOUR_DOMAIN
from MySQLdb import Connect
from helpfunctions import check_session, convert_str

environment = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, 'templates')))

cookstr = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cookstr)

is_loged = check_session(cookies)

form = cgi.FieldStorage()


if not (is_loged):
    link_to_redirect = YOUR_DOMAIN + 'login.py'
    print('Refresh: 0; %s' % link_to_redirect)

elif 'author' in form:
    conn = Connect(**DATA_TO_LOGIN_TO_DB)
    curs = conn.cursor()
    is_row_exists = curs.execute('''SELECT NULL FROM authors WHERE author_id = %s;
                                ''' % (form['author'].value))
    if not is_row_exists:
        template = environment.get_template("update_db_error.html")
        errors = ['Row does not exists']
        link_to_redirect = YOUR_DOMAIN + 'add_author.py'
        print(cookies)
        print('Refresh: 5; %s' % link_to_redirect)
        print(template.render(errors=errors))

    else:
        curs.execute('''DELETE FROM authors WHERE author_id=%s;    
                    ''' % (form['author'].value))
        conn.commit()
        template = environment.get_template("update_db_success.html")
        actions = ['Row was deleted.']
        link_to_redirect = YOUR_DOMAIN + 'add_author.py'
        print(cookies)
        print('Refresh: 5; %s' % link_to_redirect)
        print(template.render(actions=actions))

elif ('first_name' in form) and ('last_name' in form):
    conn = Connect(**DATA_TO_LOGIN_TO_DB)
    curs = conn.cursor()
    curs.execute('''INSERT INTO authors (first_name, last_name) 
                    VALUES (%s, %s);
                ''' % (convert_str(form['first_name'].value), convert_str(form['last_name'].value)))
    conn.commit()
    template = environment.get_template("update_db_success.html")
    actions = ['Row was added.']
    link_to_redirect = YOUR_DOMAIN + 'add_author.py'
    print(cookies)
    print('Refresh: 5; %s' % link_to_redirect)
    print(template.render(actions=actions))


elif os.environ['REQUEST_METHOD'] == 'GET':
    template = environment.get_template("add_author.html")
    conn = Connect(**DATA_TO_LOGIN_TO_DB)
    curs = conn.cursor()
    curs.execute('''SELECT author_id, CONCAT(first_name, ' ', last_name) AS full_name FROM authors;    
                 ''')
    columns_names = [i[0] for i in curs.description]
    authors = curs.fetchall()
    authors = [dict(zip(columns_names, row)) for row in authors]

    print(cookies)
    print(template.render(authors=authors))




