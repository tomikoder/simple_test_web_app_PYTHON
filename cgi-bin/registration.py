#!/usr/bin/python
""

from jinja2 import Environment, FileSystemLoader
import os
import http.cookies, os, cgi
from form_validator import login_validate_form_data
from MySQLdb import Connect
from settings import DATA_TO_LOGIN_TO_DB, PROJECT_DIR, YOUR_DOMAIN
from helpfunctions import convert_str
import uuid

environment = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, 'templates')))

if os.environ['REQUEST_METHOD'] == 'GET':
    template = environment.get_template("registration.html")
    print(template.render())

elif os.environ['REQUEST_METHOD'] == 'POST':
    form = cgi.FieldStorage()
    errors = login_validate_form_data(form)
    if errors:
        template = environment.get_template("registration.html")
        print(template.render(errors=errors))
    else:
        conn = Connect(**DATA_TO_LOGIN_TO_DB)
        curs = conn.cursor()
        mail = convert_str(form['mail'].value)
        password = convert_str(form['pass'].value)
        test = curs.execute('''SELECT NULL FROM users WHERE email = %s; 
                            ''' % (mail))
        if (test):
            template = environment.get_template("registration.html")
            print(template.render(errors=["Email już jest w bazie danych"]))
        else:
            curs.execute('''INSERT INTO users (email, password)
                                       VALUES (%s, %s);
                         ''' % (mail, password))
            conn.commit()

            curs.execute('''SELECT user_id FROM users
                            WHERE email = %s;
                         ''' % (mail))

            user_id = curs.fetchone()[0]


            new_session = str(uuid.uuid1())

            curs.execute('''INSERT INTO sessions (session_id, user_id, expire_time)
                                         VALUES  (%s, %s, DATE_ADD(now() , INTERVAL 1 HOUR));
                                ''' % (convert_str(new_session), user_id))

            conn.commit()

            cookies = http.cookies.SimpleCookie()
            cookies['user'] = user_id
            cookies['session'] = new_session

            link_to_redirect = YOUR_DOMAIN + 'menu.py'
            print(cookies)
            print('Refresh: 0; %s' % link_to_redirect)












