# Считайте файл согласно вашему варианту.
# В строках имеются пропуски, обозначенные «NA» – замените их, рассчитав среднее значение соседних чисел.
# Проведите фильтрацию данных в рамках каждой строки тем способом,
# который соответствует вашему варианту, а также результирующую операцию и ее вывод в текстовый файл.
# Вариант 7
# Оставляем положительные значения, квадрат которых не превышает 2500
# Среднее по каждой строке
lines = open('third_task.txt','r').readlines()
res = []
# сумма всех чисел, квадрат которых меньше 2500 и с заменой NA на среднее соседей
for line in lines:
    nums = []
    parts = line.split()
    for i, val in enumerate(parts):
        if val == 'N/A': nums.append(float(parts[i-1]) + float(parts[i+1]) // 2)
        else: nums.append(float(val))
    nums = [x for x in nums if abs(x) < 50.0 and x > 0]
    res.append(0 if len(nums) == 0 else sum(nums) / len(nums))
open('third_task_result.txt','w').writelines([f'{x}\n' for x in res])