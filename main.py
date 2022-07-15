import requests
from bs4 import BeautifulSoup
import time
import datetime
from datetime import datetime

arr = []
animals = []
symbols = {}
key = 0
Len = 0
cnt = 0
flag = True
tests = [
    {'data': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'data': {'lesson': [1594702800, 1594706400], #1594702807?????????
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

print('---------------------------------Задание 1--------------------------------')


def find(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    print('Такого элемента нет!')
    return -1


print('Введите размер массива')
while True:
    try:
        Len = int(input())
        break
    except Exception:
        print('Введите целое число!')
print('Введите элементы массива:')
arr = [input() for _ in range(Len)]
print('Вы ввели:', arr)
print('Введите искомое:')
key = input()
print('Индекс первого искомого элемента:', find(arr, key))

print('')
print('---------------------------------Задание 2--------------------------------')
url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
page = requests.get(url).text
print('Подождите немного, идет загрузка')
while flag == True:
    soup = BeautifulSoup(page, 'xml')
    links = soup.find('div', id='mw-pages').find_all('a')
    for a in links:
        if a.text == 'Aaaaba':
            flag = False
        else:
            animals.append(a.text)
        if a.text == 'Следующая страница':
            url = 'https://ru.wikipedia.org/' + a.get('href')
            page = requests.get(url).text

print('Список получен')
print('Идет форматирование списка')
for i in animals:
    if i == 'Следующая страница' or i == 'Предыдущая страница':
        animals.remove(i)

alphabet_lower = [chr(ord("а") + i) for i in range(32)]
alphabet_upper = [chr(ord("А") + i) for i in range(32)]
for animal in animals:
    symbol = animal.strip()[0]

    if symbol not in alphabet_upper and symbol not in alphabet_lower:
        continue

    if symbol not in symbols.keys():
      symbols[symbol] = 0

    symbols[symbol] += 1

for k, v in sorted(symbols.items()):
  print(f"Буква {k}: {v}")
time.sleep(5)
print('')
print('---------------------------------Задание 3--------------------------------')


def appearance(data):
    global cnt
    lesson = data.get('lesson')
    teacher = data.get('tutor')
    student = data.get('pupil')
    teacher.sort()
    student.sort()
    teacher[0] = lesson[0] if lesson[0] > teacher[0] else teacher[0]
    teacher[-1] = lesson[-1] if lesson[-1] < teacher[-1] else teacher[-1]
    new_teacher = []
    new_student = []
    new_lesson = []
    new_lesson.append(datetime.fromtimestamp(lesson[0]))
    new_lesson.append(datetime.fromtimestamp(lesson[1]))

    for i in range(0, len(teacher), 2):
        if teacher[i] < lesson[1] and teacher[i+1] > lesson[0]:
            new_teacher.append({
                'start': datetime.fromtimestamp(teacher[i] if teacher[i] >= lesson[0] else lesson[0]),
                'end': datetime.fromtimestamp(teacher[i+1] if teacher[i+1] <= lesson[1] else lesson[1])
            })

    for i in range(0, len(student), 2):
        if student[i] < lesson[1] and student[i+1] > lesson[0]:
            new_student.append({
                #'start': datetime.fromtimestamp(student[i] if student[i] <= lesson[1] else lesson[1]),
                'start': datetime.fromtimestamp(student[i] if student[i] >= lesson[0] else lesson[0]),
                'end': datetime.fromtimestamp(student[i+1] if student[i+1] <= lesson[1] else lesson[1])
            })
    if len(new_teacher) > len(new_student):
        intervals = list(new_teacher)
        big_intervals = [
            i for i in new_student if i['start'] >= intervals[0]['start'] or i['end'] <= intervals[-1]['end']
        ]
    else:
        intervals = list(new_student)
        big_intervals = [
            i for i in new_teacher if i['start'] >= intervals[0]['start'] or i['end'] <= intervals[-1]['end']
        ]
    new_intervals = []

    for i in range(0, len(intervals)):
        for j in range(0, len(big_intervals)):
            a = intervals[i]['start']
            b = intervals[i]['end']
            c = big_intervals[j]['start']
            d = big_intervals[j]['end']
            if c == a:
                if d == b:
                    prom = a - b
                    sec = prom.total_seconds()
                    new_intervals.append(sec)
                elif d < b:
                    prom = (b - a) - (b - d)
                    sec = prom.total_seconds()
                    new_intervals.append(sec)
                elif d > b:
                    prom = (d - c) - (d - b)
                    sec = prom.total_seconds()
                    new_intervals.append(sec)
            elif b == d:
                if c > a:
                    prom = (b - a) - (c - a)
                    sec = prom.total_seconds()
                    new_intervals.append(sec)
                elif a > c:
                    prom = (d - c) - (a - c)
                    sec = prom.total_seconds()
                    new_intervals.append(sec)
            elif a > c:
                if d > b:
                    prom = (d - c) - ((a - c) + (d - b))
                    sec = prom.total_seconds()
                    new_intervals.append(sec)
                elif a < d < b:
                    prom = (d - c) - (a - c)
                    sec = prom.total_seconds()
                    new_intervals.append(sec)
            elif c > a:
                if d < b:
                    prom = (b - a) - ((c - a) + (b - d))
                    sec = prom.total_seconds()
                    new_intervals.append(sec)
                elif c < b < d:
                    prom = (d - c) - (d - b)
                    sec = prom.total_seconds()
                    new_intervals.append(sec)
            elif a >= d or c >= b:
                continue
    return sum(new_intervals)


for i, test in enumerate(tests):
  test_answer = appearance(test['data'])
  print(test_answer)

