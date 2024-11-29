from bs4 import BeautifulSoup
import pandas as pd
import os


data = []

def fill_data(path):
    global data
    soup = BeautifulSoup(open(path, 'r', encoding='utf-8').read(), 'html.parser')
    products = soup.find_all('div', class_='product-item')
    for product in products:
        name = product.find('span').text
        
        # Find price without bonuses
        price = product.find('price').text.split('₽')[0].replace(' ', '')
        price = int(price.replace(',', ''))

        # Parse characteristics
        characteristics = {}
        for characteristic in product.find_all('li'):
            type = characteristic.get('type')
            value = characteristic.text.strip()
            characteristics[type] = value

        temp = {
            'name': name,
            'price': price,
            'ram': characteristics.get('ram', None),
            'processor': characteristics.get('processor', None),
            'sim': characteristics.get('sim', None),
            'matrix': characteristics.get('matrix', None),
            'resolution': characteristics.get('resolution', None),
            'camera': characteristics.get('camera', None),
            'acc': characteristics.get('acc', None),
        }

        if temp['ram']:
            temp['ram'] = int(temp['ram'].strip()[:-2])
        if temp['price']:
            temp['price'] = int(temp['price'])
        
        data.append(temp)


for filename in os.listdir('./2'):
    if filename.endswith(".html"):
        fill_data(os.path.join('./2', filename))


df = pd.DataFrame(data)

df.set_index('name', inplace=True)

df = df.sort_values('name')
df.to_json(open('second_result.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')

df2 = df[df['price'] > 50_000]
df2.to_json(open('second_result_2.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')


print(df['price'].min(), df2['price'].max(), df2['price'].mean(), df2['price'].sum())

print(df['matrix'].value_counts())

print(df)