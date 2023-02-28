from jinja2 import Environment, FileSystemLoader
import http.cookies, os, cgi
from settings import DATA_TO_LOGIN_TO_DB, PROJECT_DIR, YOUR_DOMAIN
from MySQLdb import Connect
from helpfunctions import check_session

environment = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, 'templates')))

cookstr = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cookstr)

is_loged = check_session(cookies)

success_login = True


if not (is_loged):

    success_login = False
    link_to_redirect = YOUR_DOMAIN + 'login.py'

    print(cookies)
    print('Refresh: 0; %s' % link_to_redirect)
    template = environment.get_template("menu.html")
    print(template.render(success_login=success_login))
else:

    environment = Environment(loader=FileSystemLoader("C:\\Users\\Tomek\\PycharmProjects\\some_project\\templates"))
    template = environment.get_template("menu.html")
    print(cookies)
    print(template.render())
