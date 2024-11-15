# Вариант 7
lines = open('second_task.txt','r').readlines()
# Сумма всех чисел квадрат которых больше 100_000 в линии
res = [sum([num for num in [abs(int(num_str)) for num_str in line.split()] if num > 316]) for line in lines]
# Выборка топ 10 строк
top10 = sorted(res, reverse=True)[:10]
open('second_task_result.txt','w').writelines([f'{x}\n' for x in top10])