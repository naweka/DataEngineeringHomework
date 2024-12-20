import sqlite3

def create_database():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.executescript('''
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        manufacturer TEXT NOT NULL
    );

    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        city TEXT NOT NULL
    );

    CREATE TABLE purchases (
        purchase_id INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        purchase_date TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    ''')
    
    conn.commit()
    conn.close()

create_database()
