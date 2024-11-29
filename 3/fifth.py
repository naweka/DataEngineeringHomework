import re
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os

data = []

single_item_pages = {
    'http://myasko28.ru/catalog/kolbasa/28/',
    'http://myasko28.ru/catalog/kolbasa/30/',
    'http://myasko28.ru/catalog/kolbasa/42/',
    'http://myasko28.ru/catalog/kolbasa/32/',
    'http://myasko28.ru/catalog/kolbasa/34/',
    'http://myasko28.ru/catalog/kolbasa/45/',
    'http://myasko28.ru/catalog/kolbasa/162/',
    'http://myasko28.ru/catalog/sosiski-sardelki/55/',
    'http://myasko28.ru/catalog/sosiski-sardelki/61/',
    'http://myasko28.ru/catalog/sosiski-sardelki/59/',
}

for item in single_item_pages:
    html = requests.get(item).text
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('div', { 'class': 'catalog-element' })
    temp = {
        'name': list(list(a[0].children)[3])[1].text.strip(),
        'price': int(list(list(list(a[0].children)[3])[3])[1].text.strip()),
        'type': 'мясо'
    }
    data.append(temp)


html = requests.get('http://myasko28.ru/catalog/pelmeni/').text
soup = BeautifulSoup(html, 'html.parser')
a = soup.find_all('div', { 'class': 'box' })
for item in a:
    temp = {
        'name': list(item.children)[3].text.strip(),
        'price': int(list(item.children)[5].text[:5].strip()),
        'type': 'полуфабрикаты'
    }
    data.append(temp)


df = pd.DataFrame(data)

df.set_index('name', inplace=True)

df = df.sort_values('name')
df.to_json(open('fifth_result.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')

df2 = df[df['price'] > 200]
df2.to_json(open('fifth_result_2.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')

print(df['price'].min(), df2['price'].max(), df2['price'].mean(), df2['price'].sum())

print(df['type'].value_counts())

print(df)