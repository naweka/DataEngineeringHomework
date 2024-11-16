# Считайте csv файл и выполните с ним определенные действия согласно вашему варианту.
# Результаты поиска значений (среднее, максимум и минимум) запишите в отдельный файл:
# каждое число на новой строке. Результаты модификаций исходного файла – в отдельный csv файл.
# Вариант 27
# 1. Удалите из таблицы столбец category
# 2. Найдите среднее арифметическое по столбцу rating
# 3. Найдите максимум по столбцу price
# 4. Найдите минимум по столбцу rating
# 5. Отфильтруйте значения, взяв только те, quantity которых больше 930

import pandas as pd
df = pd.read_csv('fourth_task.txt')
df.drop(columns=['category'], inplace=True)

with open('fourth_task_results.txt', 'w') as f:
    f.write(f'{df["rating"].mean()}\n')
    f.write(f'{df["price"].max()}\n')
    f.write(f'{df["rating"].min()}\n')

df = df[df['quantity'] > 930]
df.to_csv('fourth_task_result.csv', index=False)
