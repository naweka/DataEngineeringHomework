import sqlite3
import csv
import pickle


def load_pkl_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def load_csv_file(filename):
    items = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            row['price'] = int(row['price'])  
            items.append(row)
    return items


def create_tables(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            author TEXT,
            genre TEXT,
            pages INTEGER,
            published_year INTEGER,
            isbn TEXT,
            rating REAL,
            views INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price INTEGER,
            place TEXT,
            date TEXT,
            FOREIGN KEY(title) REFERENCES books(title)
        )
    ''')
    db.commit()

def insert_books(db, books):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT OR IGNORE INTO books (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES (:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views)
    ''', books)
    db.commit()


def insert_sales(db, sales):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO sales (title, price, place, date)
        VALUES (:title, :price, :place, :date)
    ''', sales)
    db.commit()


def query_total_revenue(db):
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT books.title, SUM(sales.price) AS total_revenue
        FROM books
        JOIN sales ON books.title = sales.title
        GROUP BY books.title
        ORDER BY total_revenue DESC
    ''')
    for row in res.fetchall():
        print(f'Книга: {row[0]}, Общая выручка: {row[1]}')

def query_offline_books(db):
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT DISTINCT books.title, books.author, books.views
        FROM books
        JOIN sales ON books.title = sales.title
        WHERE sales.place = 'offline'
        ORDER BY books.views DESC
    ''')
    for row in res.fetchall():
        print(f'Книга: {row[0]}, Автор: {row[1]}, Просмотры: {row[2]}')


def query_high_rating_books(db):
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT books.title, books.rating, books.author
        FROM books
        WHERE books.rating > 4.0
    ''')
    books = res.fetchall()
    for book in books:
        print(f'Книга: {book[0]}, Рейтинг: {book[1]}, Автор: {book[2]}')

db = sqlite3.connect('books_sales.db')
create_tables(db)

books = load_pkl_file('item.pkl')
sales = load_csv_file('subitem.csv')

insert_books(db, books)
insert_sales(db, sales)

print('Общая выручка по книгам:')
query_total_revenue(db)

print('\nКниги, продававшиеся оффлайн, отсортированные по просмотрам:')
query_offline_books(db)

print('\nКниги с рейтингом выше 4.0:')
query_high_rating_books(db)