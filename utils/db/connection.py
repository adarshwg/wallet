import sqlite3
import os
db_path = os.path.join(os.path.dirname(__file__), 'database.sqlite')
conn = sqlite3.connect(db_path)

# conn = sqlite3.connect('utils/db/database.sqlite')
# conn = sqlite3.connect('databasee.sqlite')
cursor = conn.cursor()
