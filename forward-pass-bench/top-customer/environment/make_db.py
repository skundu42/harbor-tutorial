import sqlite3

db = sqlite3.connect("/app/shop.db")
db.executescript("""
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL);

INSERT INTO customers VALUES (1, 'Ada'), (2, 'Grace'), (3, 'Linus');
INSERT INTO orders (customer_id, amount) VALUES
  (1, 20), (1, 25), (1, 30), (1, 15),
  (2, 400), (2, 35),
  (3, 120), (3, 80), (3, 60);
""")
db.commit()
