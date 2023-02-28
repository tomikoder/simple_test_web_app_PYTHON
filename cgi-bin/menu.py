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
    print(cookies)
    print(template.render(email=email))
