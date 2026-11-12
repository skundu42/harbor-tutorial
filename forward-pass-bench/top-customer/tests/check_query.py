import sqlite3
import sys

query = open("/app/query.sql").read()
rows = sqlite3.connect("/app/shop.db").execute(query).fetchall()
print("query returned:", rows)

sys.exit(0 if rows and rows[0][0] == "Grace" else 1)
