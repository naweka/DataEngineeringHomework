import pandas as pd
from pymongo import MongoClient

def parse_text_file(filename):
    records = []
    current_record = {}
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '=====':
                if current_record:
                    records.append(current_record)
                    current_record = {}
            elif '::' in line:
                key, value = line.split('::', 1)
                current_record[key] = value
    
    if current_record:
        records.append(current_record)
    
    return pd.DataFrame(records)

df1 = parse_text_file('_part_1.text')
df1['explicit'] = df1['explicit'].map({'True': 1, 'False': 0})
df1['duration_ms'] = pd.to_numeric(df1['duration_ms'])
df1['year'] = pd.to_numeric(df1['year'])
df1['tempo'] = pd.to_numeric(df1['tempo'])
df1['loudness'] = pd.to_numeric(df1['loudness'])
df1['instrumentalness'] = pd.to_numeric(df1['instrumentalness'])
df1['key'] = 0
df1['energy'] = 0.5



df2 = pd.read_csv('_part_2.csv', sep=';')
df2['explicit'] = False 
df2['instrumentalness'] = 0.0

df = pd.concat([df1, df2])

client = MongoClient('mongodb://localhost:27017/')
try:
    client.drop_database('testdb2')
except Exception as e:
    print(e)
db = client['testdb2']
collection = db['test_collection2']

collection.insert_many(df.to_dict(orient='records'))

from pprint import pprint
def print_and_save(s, i):
    pprint(s)
    df = pd.DataFrame.from_dict(s)
    df.to_json(f'{i}.json', orient='records', indent=1, default_handler=str, force_ascii=False)


#-------------------------- выборка

# топ 10 самых быстрых (по темпу) треков
result = list(collection.find().sort('tempo', -1).limit(10))
print_and_save(result, 1)

# топ 10 самых быстрых треков с 2018 года
result = list(collection.find({'year': {'$gte': 2018}}).sort('tempo', -1).limit(10))
print_and_save(result, 2)

# все Lil исполнители
result = list(collection.find({'artist': {'$regex': 'Lil '}}))
print_and_save(result, 3)

# все rock песни
result = list(collection.find({'genre': {'$regex': 'rock'}}))
print_and_save(result, 4)

# топ 10 самых коротких треков
result = list(collection.find().sort('duration_ms', 1).limit(10))
print_and_save(result, 5)

#-------------------------- выбора с агрегацией  

# минимальная, средняя, максимальная длина трека
query = [
    {'$group': {
        '_id': None,
        'min_duration': {'$min': '$duration_ms'},
        'avg_duration': {'$avg': '$duration_ms'},
        'max_duration': {'$max': '$duration_ms'}
    }}
]
result = list(collection.aggregate(query))
print_and_save(result, 6)

# средняя длина трека по году
query = [
    {'$group': {
        '_id': '$year',
        'avg_duration': {'$avg': '$duration_ms'},
    }},
    {'$sort': {'_id': -1}}
]
result = list(collection.aggregate(query))
print_and_save(result, 7)

# средняя темп трека по году
query = [
    {'$group': {
        '_id': '$year',
        'avg_duration': {'$avg': '$tempo'},
    }},
    {'$sort': {'_id': -1}}
]
result = list(collection.aggregate(query))
print_and_save(result, 8)

# все треки с темпом выше 180 и старее 2015
query = [
    {'$match': {'$and': [
        {'tempo': {'$gt': 180}},
        {'year': {'$lt': 2015}},
    ]}}
]
result = list(collection.aggregate(query))
print_and_save(result, 9)

# минимальная, средняя, максимальная energy трека
query = [
    {'$group': {
        '_id': None,
        'min_energy': {'$min': '$energy'},
        'avg_energy': {'$avg': '$energy'},
        'max_energy': {'$max': '$energy'}
    }}
]
result = list(collection.aggregate(query))
print_and_save(result, 10)

#-------------------------- обновление/удаление данных 

# когда Роскомнадзор запретит explicit контент, его надо будет удалить
collection.delete_many({'explicit': 1})

# с Новым Годом! Увеличиваем всем год
collection.update_many({}, {'$inc': {'year': 1}})

# фикс неправильных значений
collection.update_many({'key': {'$gte': 12}}, {'$set': {'key': 0}})

# все Lil'ы больше не в моде
collection.delete_many({'artist': {'$regex': 'Lil '}})

# очистка базы данных от запрещённых слов
collection.delete_many({'$or': [
    {'song': {'$regex': 'nigg'}},
    {'artist': {'$regex': 'nigg'}}
]})