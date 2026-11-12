`/app/shop.db` is a SQLite database with two tables:

- `customers(id, name)`
- `orders(id, customer_id, amount)`

Write one SQL query to `/app/query.sql` that returns the name of the customer
with the highest total order amount.
