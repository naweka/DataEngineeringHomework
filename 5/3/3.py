from pymongo import MongoClient
import pandas as pd
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client['testdb1']
collection = db['test_collection1']

data = pd.read_csv('task_3_item.csv', delimiter=';', encoding='utf-8').to_dict(orient='records')

collection.insert_many(data)

# удаление по salary < 25 000 || salary > 175000
collection.delete_many({'$or':
                            [{'salary': {'$lt': 25000}},
                             {'salary': {'$gt': 175000}}]
                        })

# инкремент age
collection.update_many({}, {'$inc': {'age': 1}})

# зп +5% по профессиям
collection.update_many({'job': {'$in': ['Учитель', 'Врач']}},
                        {'$mul': {'salary': 1.05}})

# зп +7% по городам
collection.update_many({'city': {'$in': ['Прага', 'Самора', 'Душанбе']}},
                       {'$mul': {'salary': 1.07}})

# за +10%
collection.update_many({
                        'job': {'$in': ['Учитель', 'Врач']},
                        'age': {'$gte': 20, '$lte': 90},
                    }, 
                    {
                        '$mul': {'salary': 1.10}
                    })

# удаление
collection.delete_many({'age': {'$gt': 80}})
