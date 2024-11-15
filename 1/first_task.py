# Вариант 7
# Я слишком глуп для регулярок, поэтому только ручной парсинг, только хардкор
delims = set(',. \'"?!\n\t\r')
# Подсчёт частоты слов
text, freq, buf = open('first_task.txt','r').read(), {}, ''
for ch in text:
    if ch in delims:
        if buf == '': continue
        if buf not in freq: freq[buf] = 0
        freq[buf] += 1
        buf = ''
    else:
        buf += ch
open('first_task_result.txt','w').writelines([f'{x}:{freq[x]}\n' for x in dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))])

# Подсчёт предложений в абзацах
indexes = [i for i,elem in enumerate(text) if elem == '\n']
delims = set('.?!')
res = [sum(1 for ch in text[left:right] if ch in delims) for right, left in zip(indexes, [0] + indexes)]
open('first_task_result2.txt','w').writelines([f'{i}:{res[i]}\n' for i in range(len(indexes))])