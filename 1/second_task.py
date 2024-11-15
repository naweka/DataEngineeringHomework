# Считайте файл тестовый согласно вашему варианту.
# Тестовый файл содержит определенное количество строк,
# в каждой из которых расположено определенное количество чисел, разделенных пробелом.
# В каждом варианте имеются указания следующего вида: сначала задается операция,
# которую необходимо произвести для каждой строки, в результате получаем одно значение для каждой строки.
# Таким образом формируется столбец, к которому нужно применить вторую указанную операцию.
# Финальный результат записываем в текстовый файл.
# Вариант 7
# Операция в рамках одной строки: суммирование только абсолютных значений всех чисел,
# квадрат которых больше 100000.
# Операция для полученного столбца: сортировка столбца по убыванию, вывод топ-10 строк.
lines = open('second_task.txt','r').readlines()
# Сумма всех чисел квадрат которых больше 100_000 в линии
# Generator Hell 🤘
res = [sum([num for num in [abs(int(num_str)) for num_str in line.split()] if num > 316]) for line in lines]
# Выборка топ 10 строк
top10 = sorted(res, reverse=True)[:10]
open('second_task_result.txt','w').writelines([f'{x}\n' for x in top10])