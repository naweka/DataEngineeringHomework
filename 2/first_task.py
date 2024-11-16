# Загрузите матрицу из файла с форматом npy.
# Подсчитайте сумму всех элементов и их среднее арифметическое,
# подсчитайте сумму и среднее арифметическое главной и побочной диагоналей матрицы.
# Найдите максимальное и минимальное значение. Полученные значения запишите в json следующего формата:
# {
#     sum: 4,
#     avr: 4,
#     sumMD: 4, // главная диагональ
#     avrMD: 5,
#     sumSD: 4, // побочная диагональ
#     avrSD: 5,
#     max: 4,
#     min: 2
# }
# Исходную матрицу необходимо нормализовать и сохранить в формате npy. 

import numpy as np
d = np.load('first_task.npy')
open('first_task_result.json', 'w').write(f'''
{{
    "sum": {d.sum()},
    "avr": {d.mean()},
    "sumMD": {np.diag(d).sum()},
    "avrMD": {np.diag(d).mean()},
    "sumSD": {np.diag(np.rot90(d)).sum()},
    "avrSD": {np.diag(np.rot90(d)).mean()},
    "max": {d.max()},
    "min": {d.min()}
}}
''')
d = np.float64(d)
d /= d.max()
np.save('first_task_result.npy', d)