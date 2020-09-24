import sqlite3
import os


DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "Poems.db"))
SQL = db.cursor()

SQL.execute("SELECT user_name, max(votes) FROM Poems;")

result = SQL.fetchall()

print(result[0][0])