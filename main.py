import requests
from bs4 import BeautifulSoup
import re
import time

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
    {'data': {'lesson': [1594702800, 1594706400],
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
time.sleep(3)

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
    print('Lesson', lesson)
    print('Teacher', teacher)
    print('Student:', student)
    if lesson[0] > teacher[0]:
        print('Учитель зашел раньше начала урока')
        print(lesson[0], '>', teacher[0])
        if teacher[1] > lesson[0]:
            print('Учитель зашел раньше начала урока и не выходил до его начала')
            print(lesson[0], '>', teacher[0])
            prom = (teacher[1] - teacher[0]) - (lesson[0] - teacher[0])
            new_start = teacher[1] - prom
            teacher[0] = new_start
        elif teacher[1] < lesson[0]:
            print('Учитель зашел и вышел раньше начала урока')
            print(teacher[1], '<', lesson[0])
            teacher.pop(0)
            teacher.pop(0)
    if teacher[-1] > lesson[1]:
        print('Учитель вышел после конца урока')
        print(teacher[-1], '>', lesson[1])
        if teacher[-2] > lesson[1]:
            print('Учитель зашел и вышел после конца урока')
            print(teacher[-2], '>', lesson[1])
            teacher.pop(-1)
            teacher.pop(-1)
        elif lesson[1] > teacher[-2]:
            print('Учитель зашел до конца урока и вышел после конца урока')
            print(lesson[1], '>', teacher[-2])
            #prom = (teacher[-1] - teacher[-2]) - (teacher[-1] - lesson[1])
            teacher[-1] = lesson[1]
        elif lesson[1] > teacher[-1]:
            print('Учитель зашел и вышел до конца урока')
            print(lesson[1], '>', teacher[-1])
    print('Teacher', teacher)
    print('Student:', student)
    print('')
    print('')
    print('')

    #print('Teacher', teacher)
    #print('Student:', student)

    for i in range(0, (len(teacher)-1)):
        for j in range(0, (len(student)-1)):
            if teacher[i] == student[j]: #если учитель и ученик зашли в одно время
                if student[j+1] == teacher[i+1]: #и вышли в одно время
                    cnt = cnt + (teacher[i+1] - teacher[i])
                    #print('1.1', cnt)
                elif teacher[i+1] > student[j+1]: #и ученик вышел раньше
                    cnt = cnt + ((teacher[i+1] - teacher[i]) - (teacher[i+1] - student[j+1]))
                    #print('1.2', cnt)
                elif student[j+1] > teacher[i+1]: #и учитель вышел раньше
                    cnt = cnt + ((teacher[i+1] - teacher[i]) - (student[j+1] - teacher[i+1]))
                    #print('1.3', cnt)
            elif teacher[i] < student[j]: #если учитель зашел на урок раньше
                if student[j+1] == teacher[i+1]: #и вышли в одно время
                    cnt = cnt + ((teacher[i+1] - teacher[i]) - (student[j] - teacher[i]))
                    #print('2.1', cnt)
                elif teacher[i + 1] > student[j + 1]:  #и ученик вышел раньше
                    cnt = cnt + ((teacher[i+1] - teacher[i]) - (student[j] - teacher[i]) - (teacher[i+1] - student[j+1]))
                    #print('2.2', cnt)
                elif student[j+1] > teacher[i+1]: #и учитель вышел раньше
                    cnt = cnt + ((teacher[i+1] - teacher[i]) - (student[i] - teacher[i]) - (student[j+1] - teacher[i+1]))
                    #print('2.3', cnt)
            elif teacher[i] > student[j]: #если ученик зашел раньше учителя
                if teacher[i+1] == student[j+1]: #и вышли в одно время
                    cnt = cnt + ((teacher[i+1] - teacher[i]) - (teacher[i] - student[j]))
                    #print('3.1', cnt)
                elif student[j+1] < teacher[i + 1]:  # и ученик вышел раньше
                    cnt = cnt + ((student[j] - student[j + 1]) - (teacher[i] - student[j]) - (teacher[i + 1] - student[j + 1]))
                    #print('3.2', cnt)
                elif student[j+1] > teacher[i+1]: #и учитель вышел раньше
                    cnt = cnt + ((student[j] - student[j + 1]) - (teacher[i] - student[j]) - (student[j + 1] - teacher[i + 1]))
                    #print('3.3', cnt)
    #print('Cnt', cnt)
    return cnt


    #global lesson_time, teacher_time, student_time
    #student = data.get('pupil')
    #for i in range(0, (len(student)-1)):
     #   student_time = student_time + (student[i+1] - student[i])
    #print('Student time:', student_time)
    #teacher = data.get('tutor')
    #for i in range(0, (len(teacher) - 1)):
     #   teacher_time = teacher_time + (student[i + 1] - student[i])
    #print('Teacher time', teacher_time)
    #return(student_time, teacher_time)


for i, test in enumerate(tests):
  test_answer = appearance(test['data'])
  #print(test_answer)

