# Найти публичный API, который возвращает JSON с некоторыми данными.
# Необходимо получить данные в формате JSON, преобразовать в html представление в зависимости от содержания.
import requests
import pandas as pd
from io import StringIO
session = requests.Session()
session.trust_env = False
df = pd.read_json(StringIO(session.get('http://jsonplaceholder.typicode.com/albums').text))
open('sixth_task_result.html', 'w').write(df.to_html())
