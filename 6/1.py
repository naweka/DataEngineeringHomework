import pandas as pd
import sys
from numpy import int16, float16
from pprint import pprint as pp
from sklearn.preprocessing import LabelEncoder
import os

print('Загрузка датасета...', end='')
df = pd.read_json('data.ndjson', lines=True)
# df = pd.read_json('data_small.ndjson')
print('OK')


# ---------------- подготовка


def unpack_dict_in_col(d, colname):
    d[colname] = d[colname].fillna('{}')
    d = d.join(pd.json_normalize(d.pop(colname)))
    return d

# удачная попытка распаковать некоторые значения
# df = df.explode('genres')
# df = unpack_dict_in_col(df, 'schedule')

# можно распаковать, но смысла большого не будет
# df = df.explode('wikiquotes')
# df = unpack_dict_in_col(df, 'rating')
# df = unpack_dict_in_col(df, 'externals')
# df = unpack_dict_in_col(df, 'image')
# df = unpack_dict_in_col(df, '_links')

# неудачная попытка распаковать некоторые значения
# df = unpack_dict_in_col(df, 'wikipedia')
# df = unpack_dict_in_col(df, 'network')
# df = unpack_dict_in_col(df, 'seasons')
# df = unpack_dict_in_col(df, 'webChannel')

# print(df)

# ---------------- первичный анализ


memory_usage_start = df.memory_usage(deep=True, index=False)
print(f'Использование памяти в исходном датасете: {memory_usage_start.sum()}')
memory_usage_start_dict = memory_usage_start.to_dict()
memory_usage_start_dict = {k: v for k, v in sorted(memory_usage_start_dict.items(), key=lambda item: -item[1])}

data = []
column_types_dict = df.dtypes.to_dict()
print('Колонка        Размер в байтах        Доля            Тип данных')
for k,v in memory_usage_start_dict.items():
    print(f'{k:<20}    {v:<15}    {int(100.0*float(v)/memory_usage_start.sum()):<15}    {column_types_dict[k]}')
    data.append({
        'col': k,
        'typ': str(column_types_dict[k]),
        'mem': v,
        'per': int(100.0*float(v)/memory_usage_start.sum())
    })
pd.DataFrame.from_dict(data).to_json('before_compression.json', indent=1, force_ascii=False, orient='records')


# ---------------- преобразования


# если пытаться распаковывать некоторые колонки, размер датасета увеличится в ~1000 раз
# columns_object_type = df.drop(['days', 'network', 'webChannel', 'wikipedia', '_embedded', 'seasons'], axis=1).select_dtypes(include=['object']).columns 
print('Получаем колонки...')
columns_object_type = df.select_dtypes(include=['object']).columns 
columns_int64_type = df.select_dtypes(include=['int64']).columns 
columns_float64_type = df.select_dtypes(include=['float64']).columns 

print('Получаем уникальные значения object колонок...')
total_rows = float(len(df))
columns_object_type = [
    x for x in columns_object_type
    if len(df[x].value_counts()) / total_rows < 0.5
]

label_encoder_dict = {
    key: value for key, value in zip(columns_object_type, [
        LabelEncoder() for _ in columns_object_type
    ])
}

print('object type')
for i,col in enumerate(columns_object_type, 1):
    # df[col] = label_encoder_dict[col].fit_transform(df[col])
    try:
        print(i, col, end=' — ')
        df[col] = label_encoder_dict[col].fit_transform(df[col])
        # df[col] = df[col].astype(int16)
        df[col] = pd.to_numeric(df[col], downcast='integer')
        print('OK')
    except:
        print('SKIPPED: LIST/DICT')

print('int64 type')
for i,col in enumerate(columns_int64_type, 1):
    print(i, col)
    # df[col] = df[col].astype(int16)
    df[col] = pd.to_numeric(df[col], downcast='integer')

print('float64 type')
for i,col in enumerate(columns_float64_type, 1):
    print(i, col)
    # df[col] = df[col].astype(float16)
    df[col] = pd.to_numeric(df[col], downcast='float')


# ---------------- вторичный анализ


memory_usage_start = df.memory_usage(deep=True, index=False)
print(f'Использование памяти в новом датасете: {memory_usage_start.sum()}')
memory_usage_start_dict = memory_usage_start.to_dict()
memory_usage_start_dict = {k: v for k, v in sorted(memory_usage_start_dict.items(), key=lambda item: -item[1])}

data = []
column_types_dict = df.dtypes.to_dict()
print('Колонка        Размер в байтах        Доля            Тип данных')
for k,v in memory_usage_start_dict.items():
    print(f'{k:<20}    {v:<15}    {int(100.0*float(v)/memory_usage_start.sum()):<15}    {column_types_dict[k]}')
    data.append({
        'col': k,
        'typ': str(column_types_dict[k]),
        'mem': v,
        'per': int(100.0*float(v)/memory_usage_start.sum())
    })
pd.DataFrame.from_dict(data).to_json('after_compression.json', indent=1, force_ascii=False, orient='records')



# df.to_pickle('result_all_columns.pkl.xz')

print('Сохранение на диск...')
# df.to_csv('result_all_columns.csv.zip')
df.to_json('result_all_columns.ndjson', orient='records')


# 37_632_746
# 33_210_926
# ___856_851