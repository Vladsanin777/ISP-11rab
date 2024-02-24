import asyncio
import sqlite3

import openpyxl
from cryptography.fernet import Fernet

key = Fernet.generate_key()
# Зашифровать строку
cipher = Fernet(key)
encrypted_string = cipher.encrypt(b"Hello, world!")

print(encrypted_string)
# Расшифровать строку
decrypted_string = cipher.decrypt(encrypted_string)

print(decrypted_string)





# Создаем базу данных
with sqlite3.connect("Easy questions on Python.db") as conn:

  # Создаем таблицу
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS Easy_questions_on_Python (
    number INTEGER,
    question TEXT,
    answer1 TEXT,
    answer2 TEXT,
    answer3 TEXT,
    key TEXT
  )
  """)

  
  # Сохраняем изменения
  conn.commit()
  



# Открываем файл Excel
wb = openpyxl.load_workbook("Лёгкие вопросы по пайтон.xlsx")

# Получаем лист с данными
sheet = wb.active
async def convert_1():
  # Цикл по строкам
  for row in range(1, (int(input("Сколько столбцов в таблице?")) + 1)):
    # Получаем три элемента из текущей строки
    yield [sheet.cell(row=row, column=col).value for col in range(1, 5)]






async def adding_to_database(*, number, question, answer1, answer2, answer3, key):
  with sqlite3.connect('Easy questions on Python.db') as db_questions:
    cursor = db_questions.cursor()
    cursor.execute("""
    INSERT INTO Easy_questions_on_Python (
      number,
      question,
      answer1,
      answer2,
      answer3,
      key) 
    VALUES (?, ?, ?, ?, ?, ?)""", (number, question, answer1, answer2, answer3, key,))
    db_questions.commit()


async def sorting(sorting: list):
  number = 1
  for i in sorting:
    key = Fernet.generate_key()
    # Зашифровать строку
    cipher = Fernet(key)
    u = []
    for p in i:
      u.append(cipher.encrypt("{}".format(p).encode('utf-8')))

    await asyncio.ensure_future(adding_to_database(number=number, question=u[0], answer1=u[1], answer2=u[2], answer3=u[3], key=key))
    number += 1



async def main():
  result = [data async for data in convert_1()]
  print(result)
  await asyncio.gather(sorting(result))

asyncio.run(main())

