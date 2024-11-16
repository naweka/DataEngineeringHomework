# Найдите набор данных (csv, json), размер которого превышает 20-30Мб.
# Отберите для дальнейшей работы в нем 7-10 полей (пропишите это преобразование в коде).
# Для полей, представляющих числовые данные, рассчитайте характеристики:
# максимальное и минимальное значения, среднее арифметическое, сумму, стандартное отклонение.
# Для полей, представляющий текстовые данные (в виде меток некоторых категорий) рассчитайте частоту встречаемости.
# Сохраните полученные расчеты в json.
# Сохраните набор данных с помощью разных форматов: csv, json, msgpack, pkl.
# Сравните размеры полученных файлов.

import json 
import pickle
import msgpack
import pandas as pd
from numpy import int64, float64
from io import BytesIO as stream

# https://catalog.data.gov/dataset/electric-vehicle-population-data
df = pd.read_csv('Electric_Vehicle_Population_Data.csv')
df = df[['VIN (1-10)', 'County', 'City', 'Model Year', 'Electric Range',
       'Base MSRP', 'Legislative District', 'DOL Vehicle ID', 'Electric Utility']]

res = {}
for col_name, dt in zip(df.columns, df.dtypes):
    if dt in [int64, float64]:
        res[col_name] = {
            'min': df[col_name].min(),
            'max': df[col_name].max(),
            'mean': df[col_name].mean(),
            'sum': df[col_name].sum(),
            'std': df[col_name].std(),
        }
    else:
        res[col_name] = {
            'freq': df[col_name].value_counts().to_dict()
        }

# https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int64):
            return int(obj)
        if isinstance(obj, float64):
            return float(obj)
        return super(NpEncoder, self).default(obj)
    
json.dump(res, open('Electric_Vehicle_Population_Data.json', 'w'), cls=NpEncoder)

s = stream()
df.to_csv(s)
csv_size = len(s.getvalue())

s.truncate(0); s.seek(0)
df.to_json(s, force_ascii=False, orient='records')
json_size = len(s.getvalue())

s.truncate(0); s.seek(0)
df.to_pickle(s)
pkl_size = len(s.getvalue())

s.truncate(0); s.seek(0)
dict_res = df.to_dict(orient='records')
packed = msgpack.packb(dict_res, use_bin_type=True)
s.write(packed)
msgpack_size = len(s.getvalue())


print('csv_size (Mib): ', csv_size / 1024.0 / 1024.0)
print('json_size (Mib): ', json_size / 1024.0 / 1024.0)
print('pkl_size (Mib): ', pkl_size / 1024.0 / 1024.0)
print('msgpack_size (Mib): ', msgpack_size / 1024.0 / 1024.0)