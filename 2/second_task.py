# Загрузите матрицу из файла с форматом npy. Создайте три массива  x,y,z.
# Отберите из матрицы значения, которые превышают следующее значение:
# (500+вариант), следующим образом: индексы элемента разнесите по массивам x,y,
# а само значение в массив z. Сохраните полученные массив в файла формата npz.
# Воспользуйтесь методами np.savez() и np.savez_compressed(). Сравните размеры полученных файлов. 

import numpy as np
from io import BytesIO as stream

x,y,z = [],[],[]
d = np.load('second_task.npy')
for i, line in enumerate(d):
    for j, val in enumerate(line):
        if val > 527:
            x.append(i); y.append(j); z.append(val)

s = stream()
np.savez(s,x,y,z)
savez_size = len(s.getvalue())

s.truncate(0); s.seek(0)
np.savez_compressed(s,x,y,z)
savez_compressed_size = len(s.getvalue())

print('np.savez size:', savez_size)
print('np.savez_compressed size:', savez_compressed_size)
print('compression ratio:', savez_compressed_size / savez_size)