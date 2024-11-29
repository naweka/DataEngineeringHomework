import pandas as pd
import os


data = []

def fill_data(path):
    global data
    lines = open(path, 'r', encoding='utf-8').readlines()
    temp = {
            'name': lines[3].strip(),
            'constellation': lines[6].strip(),
            'spectral_class': lines[9].strip(),
            'radius': int(lines[12].strip()),
            'rotation': lines[15].strip(),
            'age': lines[18].strip(),
            'distance': lines[21].strip(),
            'absolute-magnitude': lines[24].strip(),
        }
        
    data.append(temp)


for filename in os.listdir('./3'):
    if filename.endswith(".xml"):
        fill_data(os.path.join('./3', filename))


df = pd.DataFrame(data)

df.set_index('name', inplace=True)

df = df.sort_values('name')
df.to_json(open('third_result.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')

df2 = df[df['radius'] > 50_000]
df2.to_json(open('third_result_2.json', 'w', encoding='utf-8'), force_ascii=False, orient='records')


print(df['radius'].min(), df2['radius'].max(), df2['radius'].mean(), df2['radius'].sum())

print(df['constellation'].value_counts())

print(df)