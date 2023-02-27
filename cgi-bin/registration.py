#!/usr/bin/python
""

from jinja2 import Environment, FileSystemLoader
import os
import http.cookies, os, cgi
from form_validator import login_validate_form_data
from MySQLdb import Connect
from settings import DATA_TO_LOGIN_TO_DB
from base64 import b64encode

cookstr = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cookstr)
usercook = cookies.get("simple_web_app_cookies")
environment = Environment(loader=FileSystemLoader("C:\\Users\\Tomek\\PycharmProjects\\some_project\\templates"))

if os.environ['REQUEST_METHOD'] == 'GET':
    if usercook == None:  # create first time
        cookies = http.cookies.SimpleCookie()
        cookies['simple_web_app_cookies'] = {}

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
        mail = form['mail'].value
        password = form['pass'].value
        test = curs.execute('SELECT EXISTS(SELECT NULL FROM persons WHERE email = %s);' % (mail))
        if not (test[0]):
            template = environment.get_template("login.html")
            print(template.render(errors=["Email już jest w bazie danych"]))
        else:
            curs.execute('''INSERT INTO users (email, password)
                                       VALUES (%s, %s);
                         ''' % (mail, password))

            session_key = os.urandom(50)
            session_key = b64encode(session_key).decode('utf-8')
            user_id = curs.execute('''
                                    SELECT user_id FROM users WHERE email = %s;
                                   ''' % (mail))[0]
            curs.execute('''INSERT INTO sessions (session_id, user_id, expire_time)''')



