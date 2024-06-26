import sqlite3
import asyncio
import os
from icecream import ic
from cryptography.fernet import Fernet
import random

class TG_Users():
  #Проверка или создание базыданных пользователей телеграмм бота
  async def tg_users_connect(self):
    try:
      with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
        cursor = db_tg_users.cursor()
        query = """CREATE TABLE IF NOT EXISTS tg_users (id INTEGER, name TEXT, premium_gpt BOOLEAN, premium_test_python BOOLEAN, proba_premium_test_python INTEGER, pofil_name TEXT, user_name TEXT, answer_python_test_number_easy INTEGER, enter_answer_python_test_number_easy INTEGER, list_answer_python_test_number_easy TEXT, answer_python_test_number_medium INTEGER, enter_answer_python_test_number_medium INTEGER, list_answer_python_test_number_medium TEXT, answer_python_test_number_hard INTEGER, enter_answer_python_test_number_hard INTEGER, list_answer_python_test_number_hard TEXT)"""
        cursor.execute(query)
        print("Соединение с базой данных tg_users.db успешно создано!")
    except Exception as e:
      print(f"1Ошибка при создании таблицы в базе данных tg_users.db: {e}")


  #Автоматическая регистрнатия нового пользователя
  async def tg_users_edit_all_newuser(self, *, id, pofil_name, user_name):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      if (cursor.execute("SELECT id FROM tg_users WHERE id = ?", (int(id),)).fetchone()) is None:
        cursor.execute("INSERT INTO tg_users (id, proba_premium_test_python, pofil_name, user_name, premium_gpt, premium_test_python, answer_python_test_number_easy, enter_answer_python_test_number_easy, list_answer_python_test_number_easy, answer_python_test_number_medium, enter_answer_python_test_number_medium, list_answer_python_test_number_medium, answer_python_test_number_hard, enter_answer_python_test_number_hard, list_answer_python_test_number_hard, name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, 3, pofil_name, user_name, False, False, 0, 0, '|', 0, 0, '|', 0, 0, '|', None,))
      else:
        cursor.execute(
          "UPDATE tg_users SET proba_premium_test_python = ?, pofil_name = ?, user_name = ?, premium_gpt = ?, premium_test_python = ?, answer_python_test_number_easy = ?, enter_answer_python_test_number_easy = ?, list_answer_python_test_number_easy = ?, answer_python_test_number_medium = ?, enter_answer_python_test_number_medium = ?, list_answer_python_test_number_medium = ?, answer_python_test_number_hard = ?, enter_answer_python_test_number_hard = ?, list_answer_python_test_number_hard = ?, name = ? WHERE id = ?",
          (3, pofil_name, user_name, False, False, 0, 0, '|', 0, 0, '|', 0, 0, '|', None, id)
        )
      db_tg_users.commit()


  #Автоматическое вормерование имени нового пользователя при регистрации
  async def tg_users_name(self, *, from_user):
    try:
      name = f"{from_user.first_name} {from_user.last_name}"
    except AttributeError:
      try:
        name = from_user.first_name
      except AttributeError:
        name = from_user.username
    return name
  

  #Метод для поиска имени пользователя
  async def tg_users_proba_name(self, *, id_tg):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      return cursor.execute("SELECT name FROM tg_users WHERE id = ?", (id_tg,)).fetchone()[0]


  #Переименование пользователя
  async def tg_users_edit_name(self, *, from_user, new_name):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      cursor.execute("UPDATE tg_users SET name = ? WHERE id = ?", (new_name, from_user.id))
      db_tg_users.commit()


      
  #Проверка на нового пользователя
  async def tg_user_poverka_new_user(self, *, id_tg):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      return cursor.execute("SELECT id FROM tg_users WHERE id = ?", (id_tg,)).fetchone()
    

  #Проверка для GPT
  async def tg_users_premium_gpt(self, *, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      return cursor.execute("SELECT premium_gpt FROM tg_users WHERE id = ?", (user_id,)).fetchone()[0]

  
  

  #Проверка для теста по Pyton
  async def tg_users_proba_and_premium_test_python(self, *, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      proba_premium_test_python, premium_test_python = cursor.execute("SELECT proba_premium_test_python, premium_test_python FROM tg_users WHERE id = ?", (user_id,)).fetchone()
      if bool(premium_test_python) is True:
        return False, "У вас премиум!",  True
      else:
        if int(proba_premium_test_python) <= 0:
          return False, False, False
        return True, f"У вас осталось {proba_premium_test_python} попыток", True
      

 

  #Проверка на номер лёгкого вопроса
  async def testing_an_Python_test(self, *, user_id: int, python_test: str):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor = db_tg.cursor()
      return cursor.execute(f"SELECT answer_python_test_number_{python_test} FROM tg_users WHERE id = ?", (user_id,)).fetchone()[0]
       
 




  #Заносит в таблицу вопрос на тему лёгкие вопросы по Python который уже был задан пользователю 
  async def list_answer_python_test_number(self, *, user_id, number, python_test):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      list_answer_python_test_number = cursor_tg.execute(
        f"SELECT list_answer_python_test_number_{python_test} FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
      list_answer_python_test_number += f"{number}|"
      cursor_tg.execute(
        f"UPDATE tg_users SET list_answer_python_test_number_{python_test} = ? WHERE id = ?",
        (list_answer_python_test_number, user_id,),
      )
      db_tg.commit()




  #Обнуление сессии лёгкого теста по python
  async def all_python_test_delete_null(self, *, user_id, python_test):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      ic(python_test)
      cursor.execute(f"UPDATE tg_users SET answer_python_test_number_{python_test} = ?, enter_answer_python_test_number_{python_test} = ?, list_answer_python_test_number_{python_test} = ? WHERE id = ?", (0, 0, "|", user_id,),)
      db_tg_users.commit()


  #Возращает статистику по сеансу лёгких вопросов по Python
  async def progress_python_test(self, *, user_id, python_test):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor_tg = db_tg_users.cursor()
      answer_python_test_number, enter_answer_python_test_number = cursor_tg.execute(
        f"""SELECT answer_python_test_number_{python_test}, enter_answer_python_test_number_{python_test} 
        FROM tg_users WHERE id = ?""",(user_id,),).fetchone()
      return f"""Всего заданий выполнено: {answer_python_test_number}/{10}\nПравильно выполнено: {enter_answer_python_test_number}/{answer_python_test_number}"""



  
  #Метод который возращает количество заданных лёгких вопросов
  async def answer_python_test_number_chek(self, *, user_id, python_test):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      return cursor.execute(f"SELECT answer_python_test_number_{python_test} FROM tg_users WHERE id = ?", (user_id,)).fetchone()[0]

    
  #Состояние премиумов
  async def check_exceptions_premium(self, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      premium_gpt, premium_test_python = cursor.execute("""SELECT premium_gpt, premium_test_python FROM tg_users WHERE id = ?""",(user_id,),).fetchone()
      if bool(premium_gpt) is True and bool(premium_test_python) is True:
        return "У вас уже были все премиумы!"
      elif bool(premium_gpt) is True:
        return "У вас уже был премиум на GPT!"
      elif bool(premium_test_python) is True:
        return "У вас уже был премиум на тест по python!"
      else:
        return "У вас небыло премиумов!"


  #Выдача промо на акаунт
  async def promo_all_tg_bd(self, user_id):
    check = await self.check_exceptions_premium(user_id)
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      cursor_tg.execute("""
        UPDATE tg_users SET 
        premium_gpt = ?, 
        premium_test_python = ?
        WHERE id = ?
        """, (True, True, user_id,),)
      db_tg.commit()
    return check
  

  #Вызывается при не правильном ответе на лёгкий вопрос по Python
  async def not_enter_questions_test_python(self, user_id, python_test):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      answer_python_test_number = cursor_tg.execute(
        f"SELECT answer_python_test_number_{python_test} FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
      cursor_tg.execute(f"""
        UPDATE tg_users SET 
        answer_python_test_number_{python_test} = ?
        WHERE id = ?
        """, (answer_python_test_number + 1, user_id,),)
      db_tg.commit()


  #Вызывается при правильном ответе на лёгкий вопрос по Python
  async def enter_questions_test_python(self, user_id, python_test):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      answer_python_test_number, enter_answer_python_test_number = cursor_tg.execute(
        f"SELECT answer_python_test_number_{python_test}, enter_answer_python_test_number_{python_test} FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()
      cursor_tg.execute(f"""
        UPDATE tg_users SET 
        answer_python_test_number_{python_test} = ?, 
        enter_answer_python_test_number_{python_test} = ? 
        WHERE id = ?
        """, (answer_python_test_number + 1, enter_answer_python_test_number + 1, user_id,),)
      db_tg.commit()


  #Проверка номера лёгкого вопроса по Python
  async def progress_python_test_number(self, *, user_id, python_test):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      return cursor_tg.execute(
        f"SELECT answer_python_test_number_{python_test} FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
  #Возращает количество правильныхответов на лёгкие вопросы по Python
  async def enter_answer_python_test_number_chek(self, *, user_id, python_test):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      return cursor_tg.execute(
        f"SELECT enter_answer_python_test_number_{python_test} FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
    
  #Вычетание попытки за  тест по python
  async def edit_proba_premium_test_python(self, *, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      proba_premium_test_python = cursor_tg.execute(
        "SELECT proba_premium_test_python FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
      cursor_tg.execute("""
        UPDATE tg_users SET 
        proba_premium_test_python = ?
        WHERE id = ?
        """, (proba_premium_test_python - 1, user_id,),)
      db_tg.commit()

  #Список использованных вопросов в сессии лёгких вопросов
  async def spisok_list_answer_python_test_number(self, *, user_id, python_test):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      spisok_list_answer_python_test_number_easy = cursor_tg.execute(
        f"SELECT list_answer_python_test_number_{python_test} FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0].split("|")
      return spisok_list_answer_python_test_number_easy
    
  #Обнуление акаунта
  async def user_null(self, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      cursor_tg.execute("""
        UPDATE tg_users SET 
        premium_gpt = ?, 
        premium_test_python = ?,
        proba_premium_test_python = ?
        WHERE id = ?
        """, (False, False, 3, user_id,),)
      db_tg.commit()
  




class DS_Users():
  #Проверка или создание базыданных пользователей телеграмм бота
  async def ds_users_connect(self):
    try:
      with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
        cursor = db_ds_users.cursor()
        query = """CREATE TABLE IF NOT EXISTS ds_users (id INTEGER, name TEXT, premium_gpt BOOLEAN, premium_test_python BOOLEAN, proba_premium_test_python INTEGER, pofil_name TEXT, user_name TEXT, answer_python_test_number_easy INTEGER, enter_answer_python_test_number_easy INTEGER, list_answer_python_test_number_easy TEXT, answer_python_test_number_medium INTEGER, enter_answer_python_test_number_medium INTEGER, list_answer_python_test_number_medium TEXT, answer_python_test_number_hard INTEGER, enter_answer_python_test_number_hard INTEGER, list_answer_python_test_number_hard TEXT)"""
        cursor.execute(query)
        print("Соединение с базой данных ds_users.db успешно создано!")
    except Exception as e:
      print(f"1Ошибка при создании таблицы в базе данных ds_users.db: {e}")

  #Автоматическая регистрнатия нового пользователя или Обнуление существующего
  async def ds_users_edit_all_newuser(self, *, id, pofil_name, user_name):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor = db_ds_users.cursor()
      if (cursor.execute("SELECT id FROM ds_users WHERE id = ?", (int(id),)).fetchone()) is None:
        cursor.execute("INSERT INTO ds_users (id, proba_premium_test_python, pofil_name, user_name, premium_gpt, premium_test_python, answer_python_test_number_easy, enter_answer_python_test_number_easy, list_answer_python_test_number_easy, answer_python_test_number_medium, enter_answer_python_test_number_medium, list_answer_python_test_number_medium, answer_python_test_number_hard, enter_answer_python_test_number_hard, list_answer_python_test_number_hard, name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, 3, pofil_name, user_name, False, False, 0, 0, '|', 0, 0, '|', 0, 0, '|', None,))
      else:
        cursor.execute(
          "UPDATE ds_users SET proba_premium_test_python = ?, pofil_name = ?, user_name = ?, premium_gpt = ?, premium_test_python = ?, answer_python_test_number_easy = ?, enter_answer_python_test_number_easy = ?, list_answer_python_test_number_easy = ?, answer_python_test_number_medium = ?, enter_answer_python_test_number_medium = ?, list_answer_python_test_number_medium = ?, answer_python_test_number_hard = ?, enter_answer_python_test_number_hard = ?, list_answer_python_test_number_hard = ?, name = ? WHERE id = ?",
          (3, pofil_name, user_name, False, False, 0, 0, '|', 0, 0, '|', 0, 0, '|', None, id)
        )
      db_ds_users.commit()


  #Автоматическое вормерование имени нового пользователя при регистрации
  async def ds_users_name(self, *, ctx):
    try:
      name = ctx.author.display_name
    except AttributeError:
      name = ctx.author.name
    return name
  

  #Метод для поиска имени пользователя
  async def ds_users_proba_name(self, *, user_id):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor = db_ds_users.cursor()
      return cursor.execute("SELECT name FROM ds_users WHERE id = ?", (user_id,)).fetchone()[0]


  #Переименование пользователя
  async def ds_users_edit_name(self, *, user_id, new_name):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor = db_ds_users.cursor()
      cursor.execute("UPDATE ds_users SET name = ? WHERE id = ?", (new_name, user_id))
      db_ds_users.commit()


      
  #Проверка на нового пользователя
  async def ds_user_poverka_new_user(self, *, id_ds):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor = db_ds_users.cursor()
      return cursor.execute("SELECT id FROM ds_users WHERE id = ?", (id_ds,)).fetchone()
    

  #Проверка для GPT
  async def ds_users_premium_gpt(self, *, user_id):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor = db_ds_users.cursor()
      return cursor.execute("SELECT premium_gpt FROM ds_users WHERE id = ?", (user_id,)).fetchone()[0]

  
  

  #Проверка для теста по Pyton
  async def ds_users_proba_and_premium_test_python(self, *, user_id):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor = db_ds_users.cursor()
      proba_premium_test_python, premium_test_python = cursor.execute("SELECT proba_premium_test_python, premium_test_python FROM ds_users WHERE id = ?", (user_id,)).fetchone()
      if bool(premium_test_python) is True:
        return False, "У вас премиум!",  True
      else:
        if int(proba_premium_test_python) <= 0:
          return False, False, False
        return True, f"У вас осталось {proba_premium_test_python} попыток", True
      

 

  #Проверка на номер лёгкого вопроса
  async def testing_an_Python_test(self, *, user_id: int, python_test: str):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor = db_ds.cursor()
      return cursor.execute(f"SELECT answer_python_test_number_{python_test} FROM ds_users WHERE id = ?", (user_id,)).fetchone()[0]
       
 




  #Заносит в таблицу вопрос на тему лёгкие вопросы по Python который уже был задан пользователю 
  async def list_answer_python_test_number(self, *, user_id, number, python_test):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor_ds = db_ds.cursor()
      list_answer_python_test_number = cursor_ds.execute(
        f"SELECT list_answer_python_test_number_{python_test} FROM ds_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
      list_answer_python_test_number += f"{number}|"
      cursor_ds.execute(
        f"UPDATE ds_users SET list_answer_python_test_number_{python_test} = ? WHERE id = ?",
        (list_answer_python_test_number, user_id,),
      )
      db_ds.commit()




  #Обнуление сессии лёгкого теста по python
  async def all_python_test_delete_null(self, *, user_id, python_test):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor = db_ds_users.cursor()
      ic(python_test)
      cursor.execute(f"UPDATE ds_users SET answer_python_test_number_{python_test} = ?, enter_answer_python_test_number_{python_test} = ?, list_answer_python_test_number_{python_test} = ? WHERE id = ?", (0, 0, "|", user_id,),)
      db_ds_users.commit()


  #Возращает статистику по сеансу лёгких вопросов по Python
  async def progress_python_test(self, *, user_id, python_test):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor_ds = db_ds_users.cursor()
      answer_python_test_number, enter_answer_python_test_number = cursor_ds.execute(
        f"""SELECT answer_python_test_number_{python_test}, enter_answer_python_test_number_{python_test} 
        FROM ds_users WHERE id = ?""",(user_id,),).fetchone()
      return f"""Всего заданий выполнено: {answer_python_test_number}/{10}\nПравильно выполнено: {enter_answer_python_test_number}/{answer_python_test_number}"""



  
  #Метод который возращает количество заданных лёгких вопросов
  async def answer_python_test_number_chek(self, *, user_id, python_test):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor = db_ds_users.cursor()
      return cursor.execute(f"SELECT answer_python_test_number_{python_test} FROM ds_users WHERE id = ?", (user_id,)).fetchone()[0]

    
  #Состояние премиумов
  async def check_exceptions_premium(self, user_id):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds_users:
      cursor = db_ds_users.cursor()
      premium_gpt, premium_test_python = cursor.execute("""SELECT premium_gpt, premium_test_python FROM ds_users WHERE id = ?""",(user_id,),).fetchone()
      if bool(premium_gpt) is True and bool(premium_test_python) is True:
        return "У вас уже были все премиумы!"
      elif bool(premium_gpt) is True:
        return "У вас уже был премиум на GPT!"
      elif bool(premium_test_python) is True:
        return "У вас уже был премиум на тест по python!"
      else:
        return "У вас небыло премиумов!"


  #Выдача промо на акаунт
  async def promo_all_ds_bd(self, user_id):
    check = await self.check_exceptions_premium(user_id)
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor_ds = db_ds.cursor()
      cursor_ds.execute("""
        UPDATE ds_users SET 
        premium_gpt = ?, 
        premium_test_python = ?
        WHERE id = ?
        """, (True, True, user_id,),)
      db_ds.commit()
    return check
  

  #Вызывается при не правильном ответе на лёгкий вопрос по Python
  async def not_enter_questions_test_python(self, user_id, python_test):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor_ds = db_ds.cursor()
      answer_python_test_number = cursor_ds.execute(
        f"SELECT answer_python_test_number_{python_test} FROM ds_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
      cursor_ds.execute(f"""
        UPDATE ds_users SET 
        answer_python_test_number_{python_test} = ?
        WHERE id = ?
        """, (answer_python_test_number + 1, user_id,),)
      db_ds.commit()


  #Вызывается при правильном ответе на лёгкий вопрос по Python
  async def enter_questions_test_python(self, user_id, python_test):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor_ds = db_ds.cursor()
      answer_python_test_number, enter_answer_python_test_number = cursor_ds.execute(
        f"SELECT answer_python_test_number_{python_test}, enter_answer_python_test_number_{python_test} FROM ds_users WHERE id = ?",
        (user_id,),
      ).fetchone()
      cursor_ds.execute(f"""
        UPDATE ds_users SET 
        answer_python_test_number_{python_test} = ?, 
        enter_answer_python_test_number_{python_test} = ? 
        WHERE id = ?
        """, (answer_python_test_number + 1, enter_answer_python_test_number + 1, user_id,),)
      db_ds.commit()


  #Проверка номера лёгкого вопроса по Python
  async def progress_python_test_number(self, *, user_id, python_test):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor_ds = db_ds.cursor()
      return cursor_ds.execute(
        f"SELECT answer_python_test_number_{python_test} FROM ds_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
  #Возращает количество правильныхответов на лёгкие вопросы по Python
  async def enter_answer_python_test_number_chek(self, *, user_id, python_test):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor_ds = db_ds.cursor()
      return cursor_ds.execute(
        f"SELECT enter_answer_python_test_number_{python_test} FROM ds_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
    
  #Вычетание попытки за  тест по python
  async def edit_proba_premium_test_python(self, *, user_id):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor_ds = db_ds.cursor()
      proba_premium_test_python = cursor_ds.execute(
        "SELECT proba_premium_test_python FROM ds_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
      cursor_ds.execute("""
        UPDATE ds_users SET 
        proba_premium_test_python = ?
        WHERE id = ?
        """, (proba_premium_test_python - 1, user_id,),)
      db_ds.commit()

  #Список использованных вопросов в сессии лёгких вопросов
  async def spisok_list_answer_python_test_number(self, *, user_id, python_test):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor_ds = db_ds.cursor()
      spisok_list_answer_python_test_number_easy = cursor_ds.execute(
        f"SELECT list_answer_python_test_number_{python_test} FROM ds_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0].split("|")
      return spisok_list_answer_python_test_number_easy
    
  #Обнуление акаунта
  async def user_null(self, user_id):
    with sqlite3.connect('datab/DS/ds_users.db') as db_ds:
      cursor_ds = db_ds.cursor()
      cursor_ds.execute("""
        UPDATE ds_users SET 
        premium_gpt = ?, 
        premium_test_python = ?,
        proba_premium_test_python = ?
        WHERE id = ?
        """, (False, False, 3, user_id,),)
      db_ds.commit()
  
  









class PythonTestBase():
  async def decoder(self, question: list):
    question_decoder = []
    # Create a Fernet key object using the encrypted key from the question
    key = Fernet(question[4])

    # Decode each question part using the key and convert back to strings
    for i in question[:4]:
      # Decode the encrypted string
      decoded_string = key.decrypt(i)

      # Convert the decoded bytes to a string
      question_decoder.append(decoded_string.decode('utf-8'))

    # Return the list of decoded question parts
    return question_decoder
  

  




  
   

class PythonTest(PythonTestBase):
  async def questions_on_python_connect(self): print("Соединение с базой данных Questions on Python.db успешно установленно!" if "Questions on Python.db" in os.listdir("datab/Python") else "Ошибка при соединения с базой данных Questions on Python.db!")

  #Возращает и расшифровывает вопрос по его номеру
  async def questions_on_test_python(self, *, number_of_questions: int, python_test):
    match python_test:
      case 'easy':
        ru_python_test = 'Лёгкие'
      case 'medium':
        ru_python_test = 'Средние'
      case 'hard':
        ru_python_test = 'Сложные'
    ic(number_of_questions)
    with sqlite3.connect('datab/Python/Questions on Python.db') as db:
      cursor = db.cursor()
      print(f"SELECT question, answer1, answer2, answer3, key FROM {ru_python_test}_вопросы_по_Python WHERE number = ?")
      u = cursor.execute(f"SELECT question, answer1, answer2, answer3, key FROM {ru_python_test}_вопросы_по_Python WHERE number = ?", (number_of_questions,)).fetchone()
      ic(u)
      return await self.decoder(u)


    
  async def quantity_str(self, python_test):
    match python_test:
      case 'easy':
        ru_python_test = 'Лёгкие'
      case 'medium':
        ru_python_test = 'Средние'
      case 'hard':
        ru_python_test = 'Сложные'
    with sqlite3.connect('datab/Python/Questions on Python.db') as db:
      return db.cursor().execute(f"SELECT COUNT(*) FROM {ru_python_test}_вопросы_по_Python").fetchone()[0]
    


class DS_Servers():
  async def ds_servers_connect(self):
    try:
      with sqlite3.connect('datab/DS/ds_servers.db') as db_ds_servers:
        cursor = db_ds_servers.cursor()
        query = """CREATE TABLE IF NOT EXISTS ds_servers (guild_id INTEGER, guild_name TEXT, premium BOOLEAN, admin_channel_id INTEGER, dover_admin BOOLEAN, event_channel_id INTEGER, admin_role_id INTEGER)"""
        cursor.execute(query)
        print("Соединение с базой данных ds_servers.db успешно создано!")
    except Exception as e:
      print(f"1Ошибка при создании таблицы в базе данных ds_servers.db: {e}")


  # Метод для проверки на новый сервер
  async def if_new_guild(self, *, guild_id):
    with sqlite3.connect('datab/DS/ds_servers.db') as db_ds_servers:
      cursor = db_ds_servers.cursor()
      guild_id = cursor.execute(
        f"SELECT guild_id FROM ds_servers WHERE guild_id = ?",
        (guild_id,),
      ).fetchone()
      return True if guild_id is None else False


  # Метод для внесения в базу данных нового сервера
  async def new_guild(self, *, guild_id, guild_name, guild_event_channel):
    with sqlite3.connect('datab/DS/ds_servers.db') as db_ds_servers:
      if await self.if_new_guild(guild_id = guild_id):
        cursor = db_ds_servers.cursor()
        cursor.execute("""INSERT INTO ds_servers (guild_id, guild_name, premium, admin_channel_id, dover_admin, event_channel_id) VALUES (?, ?, ?, ?, ?, ?)""", (guild_id, guild_name, False, 0, False, guild_event_channel,))
        db_ds_servers.commit()
        return True
      return False

  # Метод для получения канала ивентов
  async def event_channel(self, *, guild_id):
    with sqlite3.connect('datab/DS/ds_servers.db') as db_ds_servers:
      cursor = db_ds_servers.cursor()
      return cursor.execute(
        f"SELECT event_channel_id FROM ds_servers WHERE guild_id = ?",
        (guild_id,),
      ).fetchone()[0]

  # Метод для изменения канала ивентов
  async def edit_event_channel(self, *, guild_id, event_channel):
    with sqlite3.connect('datab/DS/ds_servers.db') as db_ds_servers:
      cursor = db_ds_servers.cursor()
      old_event_channel = cursor.execute(
        f"SELECT event_channel_id FROM ds_servers WHERE guild_id = ?",
        (guild_id,),
      ).fetchone()[0]
      cursor.execute(f"UPDATE ds_servers SET event_channel_id = ? WHERE guild_id = ?", (event_channel, guild_id,),)
      db_ds_servers.commit()
      return old_event_channel

  # Метод для получения канала администратора
  async def admin_channel(self, *, guild_id):
    with sqlite3.connect('datab/DS/ds_servers.db') as db_ds_servers:
      cursor = db_ds_servers.cursor()
      return cursor.execute(
        f"SELECT admin_channel_id FROM ds_servers WHERE guild_id = ?",
        (guild_id,),
      ).fetchone()[0]

  # Метод для изменения канала администрации
  async def edit_admin_channel(self, *, guild_id, admin_channel):
    with sqlite3.connect('datab/DS/ds_servers.db') as db_ds_servers:
      cursor = db_ds_servers.cursor()
      old_admin_channel = cursor.execute(
        f"SELECT admin_channel_id FROM ds_servers WHERE guild_id = ?",
        (guild_id,),
      ).fetchone()[0]
      cursor.execute(f"UPDATE ds_servers SET admin_channel_id = ? WHERE guild_id = ?", (admin_channel, guild_id,),)
      db_ds_servers.commit()
      return old_admin_channel

  # Метод для изменения роли администратора
  async def edit_admin_role(self, *, guild_id, admin_role_id):
    with sqlite3.connect('datab/DS/ds_servers.db') as db_ds_servers:
      cursor = db_ds_servers.cursor()
      cursor.execute(f"UPDATE ds_servers SET admin_role_id = ? WHERE guild_id = ?", (admin_role_id, guild_id,),)
      db_ds_servers.commit()

  async def admin_role(self, guild_id):
    with sqlite3.connect('datab/DS/ds_servers.db') as db_ds_servers:
      cursor = db_ds_servers.cursor()
      return cursor.execute(
        f"SELECT admin_role_id FROM ds_servers WHERE guild_id = ?",
        (guild_id,),
      ).fetchone()[0]


class ORM(TG_Users, PythonTest, DS_Users, DS_Servers):
  def __init__(self):
    print("Начало запуска баз данных! ")
    asyncio.ensure_future(self.ds_servers_connect())
    asyncio.ensure_future(self.ds_users_connect())
    asyncio.ensure_future(self.tg_users_connect())
    asyncio.ensure_future(self.questions_on_python_connect())
