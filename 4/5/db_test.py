import sqlite3
import json


conn = sqlite3.connect('db.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM products WHERE category = "Electronics" ORDER BY price LIMIT 2;')
query1 = cursor.fetchall()

cursor.execute('SELECT city, COUNT(*) FROM customers GROUP BY city;')
query2 = cursor.fetchall()

cursor.execute('''
SELECT AVG(p.price * pu.quantity) AS avg_spent
FROM purchases pu
JOIN products p ON pu.product_id = p.product_id
WHERE p.category = 'Home Appliances';
''')
query3 = cursor.fetchone()

# ------

cursor.execute('UPDATE customers SET city = "San Francisco" WHERE customer_id = 3;')
conn.commit()

# ------

cursor.execute('SELECT * FROM purchases WHERE quantity > 1;')
query4 = cursor.fetchall()

cursor.execute('SELECT * FROM products ORDER BY price DESC LIMIT 1;')
query5 = cursor.fetchone()

cursor.execute('''
SELECT purchase_date, COUNT(*)
FROM purchases
GROUP BY purchase_date
ORDER BY COUNT(*) DESC;
''')
query6 = cursor.fetchall()

results = {
    'query1': query1,
    'query2': query2,
    'query3': query3,
    'query4': query4,
    'query5': query5,
    'query6': query6
}
with open('results.json', 'w') as file:
    json.dump(results, file, indent=1)