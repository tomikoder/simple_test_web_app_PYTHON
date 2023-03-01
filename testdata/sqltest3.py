from MySQLdb import Connect
from helpfunctions import convert_str



conn = Connect(host='localhost', user='root', passwd='kurdefaja34', port=4000, database='testDB')
curs = conn.cursor()

curs.execute('''SELECT GROUP_CONCAT(CAST(a.author_id AS CHAR), ' ') AS authors_id, GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name), ' ') AS authors, b.* FROM authors AS a INNER JOIN authors_books AS ab ON a.author_id = ab.author_id
                                                          INNER JOIN books AS b ON b.book_id = ab.book_id
                                                          GROUP BY b.book_id;    
             ''')
columns_names = [i[0] for i in curs.description]
books = curs.fetchall()
result_data = [dict(zip(columns_names, row)) for row in books]
for row in result_data:
    row_to_process = row['authors'].split(',')
    row['authors'] = row_to_process
    for idx in range(len(row_to_process)):
        row_to_process[idx] = row_to_process[idx].rstrip()
    row_to_process = ', '.join(row_to_process)
    row['authors'] = row_to_process
    print(result_data)


