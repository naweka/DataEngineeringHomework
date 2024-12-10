import sqlite3
import csv
import json
from statistics import mean

def create_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subitem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price INTEGER,
            place TEXT,
            date TEXT
        )
    ''')
    db.commit()

def load_data_from_csv(filename):
    items = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            items.append({
                'title': row['title'],
                'price': int(row['price']),
                'place': row['place'],
                'date': row['date']
            })
    return items


def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO subitem (title, price, place, date)
        VALUES (:title, :price, :place, :date)
    ''', items)
    db.commit()


def query_sorted_to_json(db, filename):
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT title, price, place, date
        FROM subitem
        ORDER BY price
        LIMIT 37
    ''')
    rows = res.fetchall()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([dict(zip(['title', 'price', 'place', 'date'], row)) for row in rows], f, ensure_ascii=False, indent=4)

def query_aggregate_price(db):
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT 
            SUM(price) AS total_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price,
            AVG(price) AS avg_price
        FROM subitem
    ''')
    result = res.fetchone()
    print(f'Вывод (суммы, мин, макс, среднее) для price \nСумма: {result[0]}, Мин: {result[1]}, Макс: {result[2]}, Среднее: {result[3]}\n')


def query_frequency_of_place(db):
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT place, COUNT(*) AS frequency
        FROM subitem
        GROUP BY place
    ''')
    results = res.fetchall()
    print ('Частота встречаемости для place')
    for row in results:
        print(f'{row[0]}, Частота: {row[1]}')


def query_filtered_sorted_to_json(db, filename):
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT title, price, place, date
        FROM subitem
        WHERE price > 1000
        ORDER BY price
        LIMIT 37
    ''')
    rows = res.fetchall()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([dict(zip(['title', 'price', 'place', 'date'], row)) for row in rows], f, ensure_ascii=False, indent=4)


db_filename = 'subitem.db'
csv_filename = 'subitem.csv'

db = sqlite3.connect(db_filename)

create_table(db)

data = load_data_from_csv(csv_filename)
insert_data(db, data)

query_sorted_to_json(db, 'sorted_subitems.json')
query_aggregate_price(db)
query_frequency_of_place(db)
query_filtered_sorted_to_json(db, 'filtered_sorted_subitems.json')
