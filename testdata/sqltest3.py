from MySQLdb import Connect
from helpfunctions import convert_str
from settings import DATA_TO_LOGIN_TO_DB



conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()

f_n = 'Adolf'
l_n = 'Hitler'
conn = Connect(**DATA_TO_LOGIN_TO_DB)
curs = conn.cursor()



