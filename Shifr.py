import asyncio
import sqlite3

import openpyxl
from cryptography.fernet import Fernet

from icecream import ic



async def main_1(data):
  # Создаем базу данных
  with sqlite3.connect("Questions on Python.db") as conn:
    cursor = conn.cursor()
    # Создаем таблицу для каждого ключа в словаре
    for sheet_name_1, rows in data.items():
      # Создаем запрос SQL для создания таблицы
      create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {sheet_name_1} (
          number INTEGER,
          question TEXT,
          answer1 TEXT,
          answer2 TEXT,
          answer3 TEXT,
          key TEXT
        )
      """
      cursor.execute(create_table_query)

      # Вставляем данные в таблицу
      insert_data_query = f"""
        INSERT INTO {sheet_name_1} (number, question, answer1, answer2, answer3, key)
        VALUES (?, ?, ?, ?, ?, ?)
      """

      for row in rows:
        cursor.execute(insert_data_query, (rows.index(row), *row,),)

    # Сохраняем изменения и закрываем соединение
    conn.commit()




async def encode_1(dict_1):
  code_1 = {}
  for sheet_name, rows in dict_1.items():
    sheet_name_1 = "_".join(sheet_name.split())
    code_3 = []
    for row in rows:
      key = Fernet.generate_key()
      code_2 = []
      for d in row:
        code_2.append(Fernet(key).encrypt(d.encode()))
      code_2.append(key)
      code_3.append(code_2) 
    code_1[sheet_name_1] = code_3
  print(code_1)
  return code_1






async def main():
  # Открываем файл Excel
  wb = openpyxl.load_workbook("Вопросы по Python.xlsx")



  # Создаем пустой словарь для хранения данных
  data = {}

  # Перебираем все листы в файле
  for sheet in wb.worksheets:
    # Добавляем имя листа в словарь
    data[sheet.title] = []

    # Перебираем все строки в листе
    for row in sheet.iter_rows():
      # Создаем список для хранения значений в строке
      new_row = []

      # Перебираем все ячейки в строке
      for cell in row:
        # Добавляем значение ячейки в список, если оно не пустое
        if cell.value is not None:
          new_row.append(cell.value)

      # Добавляем строку в список только если она не пустая
      if new_row:
        data[sheet.title].append(new_row)

  # Выводим словарь
  print(data)
  await main_1(await encode_1(data))

asyncio.run(main())

