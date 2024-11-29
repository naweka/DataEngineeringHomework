import os
import json
import xml.etree.ElementTree as ET
import pandas as pd


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    clothing_items = []
    for clothing in root.findall('clothing'):
        item = {}
        for child in clothing:
            if child.tag == 'price':
                item[child.tag] = int(child.text.strip()) if child.text else None
            else:
                item[child.tag] = child.text.strip() if child.text else None
        clothing_items.append(item)
    return clothing_items


data = []
for file_name in os.listdir('./4'):
    if file_name.endswith('.xml'):
        file_path = os.path.join('./4', file_name)
        clothing_items = parse_xml(file_path)
        data.extend(clothing_items)


df = pd.DataFrame(data)

df.set_index('name', inplace=True)

df = df.sort_values('name')
df.to_json(open('fourth_result.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')

df2 = df[df['price'] > 50_000]
df2.to_json(open('fourth_result_2.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')


print(df['price'].min(), df2['price'].max(), df2['price'].mean(), df2['price'].sum())

print(df['category'].value_counts())

print(df)