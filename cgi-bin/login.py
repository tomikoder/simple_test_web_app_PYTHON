#!/usr/bin/python
"""
"""
from jinja2 import Environment, FileSystemLoader
import http.cookies, os, cgi
from form_validator import login_validate_form_data
from settings import DATA_TO_LOGIN_TO_DB, PROJECT_DIR, YOUR_DOMAIN
from MySQLdb import Connect
from helpfunctions import convert_str, check_session
import uuid

environment = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, 'templates')))

cookstr = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cookstr)


success_login = False


is_loged = check_session(cookies)


if (is_loged):

    success_login = True
    link_to_redirect = YOUR_DOMAIN + 'menu.py'

    print(cookies)
    print('Refresh: 0; %s' % link_to_redirect)
    template = environment.get_template("login.html")
    print(template.render(success_login=success_login))


elif os.environ['REQUEST_METHOD'] == 'GET':

    template = environment.get_template("login.html")
    print(cookies)
    print(template.render(success_login=success_login))

elif os.environ['REQUEST_METHOD'] == 'POST':
    form = cgi.FieldStorage()
    errors = login_validate_form_data(form)
    if errors:
        template = environment.get_template("login.html")
        print(template.render(errors=errors))
    else:

        conn = Connect(**DATA_TO_LOGIN_TO_DB)
        curs = conn.cursor()
        mail = convert_str(form['mail'].value)
        password = convert_str(form['pass'].value)
        row_exists = curs.execute('SELECT user_id FROM users WHERE email = %s AND password = %s;' % (mail, password))
        if row_exists:
            user_id = curs.fetchone()[0]
            curs.execute('''UPDATE users 
                        SET is_loged = TRUE
                        WHERE user_id = %s;
                        ''' % (user_id))
            new_session = str(uuid.uuid1())
            curs.execute('''UPDATE sessions
                            SET session_id = %s, expire_time = DATE_ADD(now() , INTERVAL 1 HOUR)
                            WHERE user_id = %s; 
                        ''' % (convert_str(new_session), user_id))
            conn.commit()

            success_login = True
            cookies = http.cookies.SimpleCookie()
            cookies['user'] = user_id
            cookies['session'] = new_session

            template = environment.get_template("login.html")
            link_to_redirect = YOUR_DOMAIN + 'menu.py'
            print(cookies)
            print('Refresh: 0; %s' % link_to_redirect)
            print(template.render(success_login=success_login))

        else:
            template = environment.get_template("login.html")
            print(cookies)
            print(template.render(errors=["Bad password or email"]))






















