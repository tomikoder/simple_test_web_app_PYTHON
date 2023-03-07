import re

def login_validate_form_data(form):
    errors = []
    if len(form.list) == 2:
        return errors
    if not 'mail' in form:
        errors.append('Please enter the email')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", form['mail'].value):
        errors.append('Invalix email syntax')
    if not 'pass' in form:
        errors.append('Please enter the password')
    return errors

def add_book_validate_form_data(form):
    errors = []
    if form['title'].value.strip() == '':
        errors.append('Please enter the title')
    return errors

