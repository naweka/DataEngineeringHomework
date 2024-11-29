from bs4 import BeautifulSoup
import pandas as pd
import os

df = pd.DataFrame(columns=['Артикул',
                           'Наличие',
                           'Название',
                           'Город',
                           'Цена',
                           'Цвет',
                           'Количество',
                           'Размеры',
                           'Рейтинг',
                           'Просмотры',])

def parse_single_file(path):
    soup = BeautifulSoup(open(path, 'r', encoding='utf-8').read(), 'html.parser')
    product_wrapper = soup.find('div', class_='product-wrapper')

    properties = {}

    # Артикул и Наличие
    span_data = product_wrapper.find('div').find('span').text.strip().split('Наличие:')
    properties['Артикул'] = span_data[0].split(':')[1].strip()
    properties['Наличие'] = span_data[1].strip()

    # Название
    properties['Название'] = product_wrapper.find('h1', class_='title').text.strip().split(':')[1].strip()

    # Город и Цена
    address_price = product_wrapper.find('p', class_='address-price').text.strip().split('Цена:')
    properties['Город'] = address_price[0].split(':')[1].strip()
    properties['Цена'] = int(address_price[1].replace('руб', '').strip())

    # Цвет, Количество, Размеры
    div_info = product_wrapper.find_all('div')[2]
    properties['Цвет'] = div_info.find('span', class_='color').text.strip().split(':')[1].strip()
    properties['Количество'] = int(div_info.find('span', class_='quantity').text.strip().replace('шт', '').split(':')[1].strip())
    properties['Размеры'] = div_info.find_all('span')[2].text.strip().split(':')[1].strip()

    # Рейтинг и Просмотры
    last_div = product_wrapper.find_all('div')[-1]
    spans = last_div.find_all('span')
    properties['Рейтинг'] = float(spans[0].text.strip().split(':')[1].strip())
    properties['Просмотры'] = int(spans[1].text.strip().split(':')[1].strip())

    return properties


# dirty stuff
counter = 0
for filename in os.listdir('./1'):
    if filename.endswith(".html"):
        properties = parse_single_file(os.path.join('./1', filename))
        df = pd.concat([df, pd.DataFrame({
            'Артикул': properties['Артикул'],
            'Наличие': properties['Наличие'],
            'Название': properties['Название'],
            'Город': properties['Город'],
            'Цена': properties['Цена'],
            'Цвет': properties['Цвет'],
            'Количество': properties['Количество'],
            'Размеры': properties['Размеры'],
            'Рейтинг': properties['Рейтинг'],
            'Просмотры': properties['Просмотры'],
            }, index=[counter])])
        counter += 1

df = df.sort_values('Рейтинг', ascending=False)
df.to_json(open('first_result.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')

df2 = df[df['Просмотры'] > 90_000]
df2.to_json(open('first_result_2.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')


print(df['Цена'].min(), df2['Цена'].max(), df2['Цена'].mean(), df2['Цена'].sum())

print(df['Цвет'].value_counts())
