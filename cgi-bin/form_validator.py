def login_validate_form_data(form):
    errors = []
    if len(form.list) == 2:
        return errors
    if not 'mail' in form:
        errors.append('Please enter the email')
    if not 'pass' in form:
        errors.append('Please enter the password')
    return errors
