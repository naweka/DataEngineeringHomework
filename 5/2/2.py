from pymongo import MongoClient
import msgpack
from pprint import pprint
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
db = client['testdb1']
collection = db['test_collection1']

records = msgpack.load(open('task_2_item.msgpack', 'rb'))

collection.insert_many(records)


# минимальная, средняя, максимальная зп
salary = [
    {'$group': {
        '_id': None,
        'min_salary': {'$min': '$salary'},
        'avg_salary': {'$avg': '$salary'},
        'max_salary': {'$max': '$salary'}
    }}
]

# количество данных по профессиям
jobs_count = [
    {'$group': {
        '_id': '$job',
        'count': {'$sum': 1}
    }}
]


# зп по городу
salary_city = [
    {'$group': {
        '_id': '$city',
        'min_salary': {'$min': '$salary'},
        'avg_salary': {'$avg': '$salary'},
        'max_salary': {'$max': '$salary'}
    }}
]


# зп по профессии
salary_job = [
    {'$group': {
        '_id': '$job',
        'min_salary': {'$min': '$salary'},
        'avg_salary': {'$avg': '$salary'},
        'max_salary': {'$max': '$salary'}
    }}
]


# возраст по городу
age_city = [
    {'$group': {
        '_id': '$city',
        'min_age': {'$min': '$age'},
        'avg_age': {'$avg': '$age'},
        'max_age': {'$max': '$age'}
    }}
]


# возраст по профессии
age_job = [
    {'$group': {
        '_id': '$job',
        'min_age': {'$min': '$age'},
        'avg_age': {'$avg': '$age'},
        'max_age': {'$max': '$age'}
    }}
]


# максимальная зп при минимальном возрасте
max_salary_min_age = [
    {'$sort': {'age': 1, 'salary': -1}},
    {'$limit': 1}
]


# минимальная зп при максимальном возрасте
min_salary_max_age = [
    {'$sort': {'age': -1, 'salary': 1}},
    {'$limit': 1}
]


# возраст по городу при зп > 50 000, отсортировать по avg
age_salary_city = [
    {'$match': {'salary': {'$gt': 50000}}},
    {'$group': {
        '_id': '$city',
        'min_age': {'$min': '$age'},
        'avg_age': {'$avg': '$age'},
        'max_age': {'$max': '$age'}
    }},
    {'$sort': {'avg_age': -1}}
]


# зп сложный фильтр
salary_age_ranges = [
    {'$match': {'$and': [
        {'$or': [
            {'age': {'$gt': 18, '$lt': 25}},
            {'age': {'$gt': 50, '$lt': 65}},
        ]},
        {'city': {'$in': ['Минск', 'Тбилиси', 'Самора', 'Афины']}},
        {'job': {'$in': ['Менеджер', 'Продавец', 'Повар', 'Водитель']}}
    ]}},
    {'$group': {
        '_id': None,
        'min_salary': {'$min': '$salary'},
        'avg_salary': {'$avg': '$salary'},
        'max_salary': {'$max': '$salary'}
    }}
]


# произвольный запрос с $match, $group, $sort
idk = [
    {'$match': {'city': 'Вильявисиоса'}},
    {'$group': {
        '_id': '$job',
        'total_salary': {'$sum': '$salary'}
    }},
    {'$sort': {'total_salary': -1}}
]


queries = [
    salary,
    jobs_count,
    salary_city,
    salary_job,
    age_city,
    age_job,
    max_salary_min_age,
    min_salary_max_age,
    age_salary_city,
    salary_age_ranges,
    idk
]



for i, query in enumerate(queries):
    result = list(collection.aggregate(query))
    print(f'Запрос {i+1}: {result}')
    df = pd.DataFrame.from_dict(result)
    df.to_json(f'{i+1}.json', orient='records', indent=1, default_handler=str, force_ascii=False)
