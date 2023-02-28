import http.cookies, os, cgi
from MySQLdb import Connect
import http.cookies, os, cgi
from settings import DATA_TO_LOGIN_TO_DB, YOUR_DOMAIN
from helpfunctions import check_session

cookstr = os.environ.get("HTTP_COOKIE")
cookies = http.cookies.SimpleCookie(cookstr)

is_loged = check_session(cookies)
if not (is_loged):
    link_to_redirect = YOUR_DOMAIN + 'login.py'
    print('Refresh: 0; %s' % link_to_redirect)

else:
    user_id = cookies['user'].value
    conn = Connect(**DATA_TO_LOGIN_TO_DB)
    curs = conn.cursor()
    curs.execute('''UPDATE users
                    SET is_loged = FALSE
                    WHERE user_id = %s;
                ''' % (user_id))
    conn.commit()
    link_to_redirect = YOUR_DOMAIN + 'login.py'
    print(cookies)
    print('Refresh: 0; %s' % link_to_redirect)






