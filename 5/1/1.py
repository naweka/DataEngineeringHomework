from pymongo import MongoClient
import pickle
import pandas as pd


client = MongoClient('mongodb://localhost:27017/')
db = client['testdb1']
collection = db['test_collection1']


data = pickle.load(open('task_1_item.pkl', 'rb'))
collection.insert_many(data)


result1 = list(collection.find().sort('salary', -1).limit(10))
print('Запрос 1:', result1)
df = pd.DataFrame.from_dict(result1)
df.to_json('1.json', orient='records', indent=1, default_handler=str, force_ascii=False)


result2 = list(collection.find({'age': {'$lt': 30}}).sort('salary', -1).limit(15))
print('Запрос 2:', result2)
df = pd.DataFrame.from_dict(result2)
df.to_json('2.json', orient='records', indent=1, default_handler=str, force_ascii=False)


city_filter = 'Картахена'
job_filter = ['Инженер', 'Косметолог', 'Повар']
result3 = list(collection.find({'city': city_filter, 'job': {'$in': job_filter}}).sort('age', 1).limit(10))
print('Запрос 3:', result3)
df = pd.DataFrame.from_dict(result3)
df.to_json('3.json', orient='records', indent=1, default_handler=str, force_ascii=False)


complex_query = [
    {'$match': {'$and': [
        {'age': {'$gte': 25, '$lte': 35}},
        {'year': {'$gte': 2019, '$lte': 2022}},
        {'$or': [
            {'salary': {'$gt': 50000, '$lte': 75000}},
            {'salary': {'$gt': 125000, '$lt': 150000}}
        ]}
    ]}},
    {'$count': 'totalRows'}
]
result4 = list(collection.aggregate(complex_query))
print('Запрос 4:', result4)
df = pd.DataFrame.from_dict(result4)
df.to_json('4.json', orient='records', indent=1, default_handler=str, force_ascii=False)