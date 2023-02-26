#!/usr/bin/python
"""
"""
from jinja2 import Environment, FileSystemLoader
import http.cookies, os, cgi
from form_validator import login_validate_form_data

cookstr = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cookstr)
usercook = cookies.get("simple_web_app_cookies")
environment = Environment(loader=FileSystemLoader("C:\\Users\\Tomek\\PycharmProjects\\some_project\\templates"))

if os.environ['REQUEST_METHOD'] == 'GET':
    if usercook == None:  # create first time
        cookies = http.cookies.SimpleCookie()
        cookies['simple_web_app_cookies'] = {}

    template = environment.get_template("login.html")

    print(template.render())

elif os.environ['REQUEST_METHOD'] == 'POST':
    form = cgi.FieldStorage()
    errors = login_validate_form_data(form)
    if errors:
        template = environment.get_template("login.html")
        print(template.render(errors=errors))










