def login_validate_form_data(form):
    errors = []
    if len(form.list) == 2:
        return errors
    if not 'mail' in form:
        errors.append('Nie wpisałeś meila')
    if not 'pass' in form:
        errors.append('Nie wpisałeś hasła')
    return errors
