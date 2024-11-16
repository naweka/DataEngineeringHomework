# Считайте фрагмент html из файла согласно варианту.
# Извлеките данные из таблицы html. Запишите полученный csv файл.

import pandas as pd
html_tables = pd.read_html('fifth_task.html', header=0, encoding='utf8')
html_tables[0].to_csv('fifth_task_result.csv', encoding='utf8')