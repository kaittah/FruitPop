import sqlite3
fruitpop_db = "fruitpop_db.db"
conn = sqlite3.connect(fruitpop_db)
c = conn.cursor()
c.execute('''CREATE TABLE score_table (name text, score int);''')
conn.commit()
conn.close()
