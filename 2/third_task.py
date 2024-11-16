# Считайте массив объектов в формате json.
# Агрегируйте информацию по каждому товару, получив следующую информацию:
# средняя цена, максимальная цена, минимальная цена.
# Сохранить полученную информацию по каждому объекту в формате json, а также в формате msgpack.
# Сравните размеры полученных файлов.

import msgpack
import pandas as pd
from io import BytesIO as stream

df = pd.read_json('third_task.json')

gb = df.groupby('name')
df_res = pd.DataFrame(columns=['name', 'mean', 'max', 'min'])
df_res['mean'] = df.groupby('name').agg({'price':'mean'})
df_res['max'] = df.groupby('name').agg({'price':'max'})
df_res['min'] = df.groupby('name').agg({'price':'min'})
df_res['name'] = df.groupby('name').groups.keys()

s = stream()
df_res.to_json(s, force_ascii=False, orient='records')
json_size = len(s.getvalue())

s.truncate(0); s.seek(0)
dict_res = df_res.to_dict(orient='records')
packed = msgpack.packb(dict_res, use_bin_type=True)
s.write(packed)
msgpack_size = len(s.getvalue())

print('json size:', json_size)
print('msgpack size:', msgpack_size)
print('compression ratio:', msgpack_size / json_size)