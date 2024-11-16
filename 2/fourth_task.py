# Считайте данные в формате pkl о товарах.
# Также считайте данные из файла формата json о новых ценах для каждого товара: 
# {
#     name: "Apple",
#     method: "add"|"sub"|"percent+"|"percent-",
#     param: 4|0.01
# }
# Обновите цены для товаров в зависимости от метода:
# "add" – добавить значение param к цене;
# "sub" – отнять значение param от цены;
# "percent+" – поднять на param % (1% = 0.01);
# "percent-" – снизить на param %.
# Сохраните модифицированные данные обратно в формат pkl.

import pickle
import pandas as pd
d = pickle.load(open('fourth_task_products.pkl','rb'))
j = pd.read_json('fourth_task_updates.json').to_dict(orient='records')

f = {
    'add': lambda x, y: x + y,
    'sub': lambda x, y: x - y,
    'percent+': lambda x, y: x * (1+(float(y)/100)),
    'percent-': lambda x, y: x * (1-(float(y)/100)),
}

for i in range(len(d)):
    d[i]['price'] = f[j[i]['method']](d[i]['price'], j[i]['param'])

pickle.dump(d, open('fourth_task_products_result.pkl', 'wb'))