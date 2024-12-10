import sqlite3
import pandas as pd
import msgpack

# Чтение файлов с данными

with open('_product_data.msgpack', 'rb') as f:
    product_data = msgpack.unpackb(f.read(), raw=False)

with open('_update_data.text', 'r') as f:
    updates = f.readlines()

conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Создание бд

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    price REAL DEFAULT 0,
    quantity INTEGER DEFAULT 0,
    category TEXT,
    fromCity TEXT,
    isAvailable BOOLEAN DEFAULT 1,
    views INTEGER DEFAULT 0,
    update_count INTEGER DEFAULT 0
);
''')
conn.commit()

# Заполнение бд данными

for product in product_data:
    cursor.execute('''
    INSERT OR IGNORE INTO products 
    (name, price, quantity, category, fromCity, isAvailable, views) 
    VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', (
        product.get('name', None), 
        product.get('price', 0.0), 
        product.get('quantity', 0), 
        product.get('category', 'Unknown'), 
        product.get('fromCity', 'Unknown'), 
        product.get('isAvailable', False), 
        product.get('views', 0)
    ))
conn.commit()

# Применение измненний к данным

for line in updates:
    try:
        name, method, param = line.strip().split('::')
        cursor.execute('SELECT * FROM products WHERE name = ?', (name,))
        product = cursor.fetchone()
        if not product:
            continue

        product_id, name, price, \
        quantity, category, fromCity, \
        isAvailable, views, update_count = product

        if method == 'price_abs':
            new_price = price + float(param)
            if new_price >= 0:
                cursor.execute('UPDATE products SET price = ?, update_count = update_count + 1 WHERE id = ?', (new_price, product_id))

        elif method == 'price_percent':
            new_price = price * (1 + float(param))
            if new_price >= 0:
                cursor.execute('UPDATE products SET price = ?, update_count = update_count + 1 WHERE id = ?', (new_price, product_id))

        elif method == 'quantity_add':
            new_quantity = quantity + int(param)
            cursor.execute('UPDATE products SET quantity = ?, update_count = update_count + 1 WHERE id = ?', (new_quantity, product_id))

        elif method == 'quantity_sub':
            new_quantity = quantity - int(param)
            if new_quantity >= 0:
                cursor.execute('UPDATE products SET quantity = ?, update_count = update_count + 1 WHERE id = ?', (new_quantity, product_id))

        elif method == 'available':
            cursor.execute('UPDATE products SET isAvailable = ?, update_count = update_count + 1 WHERE id = ?', (int(param == 'True'), product_id))

        elif method == 'remove':
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))

    except:
        continue

conn.commit()

# Анализ полученных данных

print('Топ-10 самых обновляемых товаров')
for row in cursor.execute('SELECT name, update_count FROM products ORDER BY update_count DESC LIMIT 10'):
    print(row)
print()


print('Анализ цен товаров')
for row in cursor.execute('''
SELECT 
    category,
    SUM(price) as total, 
    MIN(price) as min_price, 
    MAX(price) as max_price, 
    AVG(price) as avg_price, 
    COUNT(*) as product_count
FROM products
GROUP BY category
'''):
    print(row)
print()

print('Анализ остатков товаров в группах (по категориям)')
for row in cursor.execute('''
SELECT 
    category, 
    SUM(quantity) as total_quantity, 
    MIN(quantity) as min_quantity, 
    MAX(quantity) as max_quantity, 
    AVG(quantity) as avg_quantity, 
    COUNT(*) as product_count
FROM products
GROUP BY category
'''):
    print(row)
print()


print('Список доступных фруктов с просмотрами более 5000')
for row in cursor.execute('SELECT name, views FROM products WHERE category = "fruit" AND isAvailable = 1 AND views > 5000'):
    print(row)

conn.close()
