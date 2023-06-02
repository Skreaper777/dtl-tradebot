"""

https://habr.com/ru/post/593065/

"""

import psycopg2
# Импортируем библиотеки
import pymorphy2

# import sklearn


# Подключаемся к PostgreSQL
conn = psycopg2.connect(dbname='energy', user='mao', password='darin', host='localhost')
cursor = conn.cursor()

# Настраиваем язык для библиотеки морфологии
morph = pymorphy2.MorphAnalyzer(lang='ru')

# объявляем массив кодов ответов и ответов
answer_id=[]
answer = dict()

# получаем из PostgreSQL список ответов и проиндексируем их.
# Работая с PostgreSQL обращаемся к схеме app, в которой находятся таблицы с данными
cursor.execute('SELECT id, answer FROM app.chats_answer;')
records = cursor.fetchall()
for row in records:
		answer[row[0]]=row[1]