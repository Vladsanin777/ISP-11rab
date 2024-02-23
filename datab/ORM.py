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
  async def tg_users_edit_all_newuser(self, *, id, pofil_name, user_name, name):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      if (cursor.execute("SELECT id FROM tg_users WHERE id = ?", (int(id),)).fetchone()) is None:
        cursor.execute("INSERT INTO tg_users (id, proba_premium_test_python, pofil_name, user_name, premium_gpt, premium_test_python, answer_python_test_number_easy, enter_answer_python_test_number_easy, list_answer_python_test_number_easy, answer_python_test_number_medium, enter_answer_python_test_number_medium, list_answer_python_test_number_medium, answer_python_test_number_hard, enter_answer_python_test_number_hard, list_answer_python_test_number_hard, name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, 3, pofil_name, user_name, False, False, 0, 0, '|', 0, 0, '|', 0, 0, '|', name,))
      else:
        cursor.execute(
          "UPDATE tg_users SET proba_premium_test_python = ?, pofil_name = ?, user_name = ?, premium_gpt = ?, premium_test_python = ?, answer_python_test_number_easy = ?, enter_answer_python_test_number_easy = ?, list_answer_python_test_number_easy = ?, answer_python_test_number_medium = ?, enter_answer_python_test_number_medium = ?, list_answer_python_test_number_medium = ?, answer_python_test_number_hard = ?, enter_answer_python_test_number_hard = ?, list_answer_python_test_number_hard = ?, name = ? WHERE id = ?",
          (3, pofil_name, user_name, False, False, 0, 0, '|', 0, 0, '|', 0, 0, '|', name, id)
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
      name = cursor.execute("SELECT name FROM tg_users WHERE id = ?", (id_tg,)).fetchone()
      return name


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
  async def testing_an_easy_Python_test(self, *, user_id: int):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor = db_tg.cursor()
      return cursor.execute("SELECT answer_python_test_number_easy FROM tg_users WHERE id = ?", (user_id,)).fetchone()[0]
       
 




  #Заносит в таблицу вопрос на тему лёгкие вопросы по Python который уже был задан пользователю 
  async def list_answer_python_test_number_easy(self, *, user_id, number):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      list_answer_python_test_number_easy = cursor_tg.execute(
        "SELECT list_answer_python_test_number_easy FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
      list_answer_python_test_number_easy += f"{number}|"
      cursor_tg.execute(
        "UPDATE tg_users SET list_answer_python_test_number_easy = ? WHERE id = ?",
        (list_answer_python_test_number_easy, user_id,),
      )
      db_tg.commit()




  #Обнуление сессии лёгкого теста по python
  async def all_easy_python_test_delete_null(self, *, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      cursor.execute("UPDATE tg_users SET answer_python_test_number_easy = ?, enter_answer_python_test_number_easy = ?, list_answer_python_test_number_easy = ? WHERE id = ?", (0, 0, "|", user_id,),)
      db_tg_users.commit()


  #Возращает статистику по сеансу лёгких вопросов по Python
  async def progress_python_test_easy(self, *, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor_tg = db_tg_users.cursor()
      answer_python_test_number_easy, enter_answer_python_test_number_easy = cursor_tg.execute(
        """SELECT answer_python_test_number_easy, enter_answer_python_test_number_easy 
        FROM tg_users WHERE id = ?""",(user_id,),).fetchone()
      return f"""Всего заданий выполнено: {answer_python_test_number_easy}/{10}\nПравильно выполнено: {enter_answer_python_test_number_easy}/{answer_python_test_number_easy}"""



  
  #Метод который возращает количество заданных лёгких вопросов
  async def answer_python_test_number_easy_chek(self, *, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      return cursor.execute("SELECT answer_python_test_number_easy FROM tg_users WHERE id = ?", (user_id,)).fetchone()[0]

    
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
  async def not_enter_questions_easy_test_python(self, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      answer_python_test_number_easy = cursor_tg.execute(
        "SELECT answer_python_test_number_easy FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
      cursor_tg.execute("""
        UPDATE tg_users SET 
        answer_python_test_number_easy = ?
        WHERE id = ?
        """, (answer_python_test_number_easy + 1, user_id,),)
      db_tg.commit()


  #Вызывается при правильном ответе на лёгкий вопрос по Python
  async def enter_questions_easy_test_python(self, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      answer_python_test_number_easy, enter_answer_python_test_number_easy = cursor_tg.execute(
        "SELECT answer_python_test_number_easy, enter_answer_python_test_number_easy FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()
      cursor_tg.execute("""
        UPDATE tg_users SET 
        answer_python_test_number_easy = ?, 
        enter_answer_python_test_number_easy = ? 
        WHERE id = ?
        """, (answer_python_test_number_easy + 1, enter_answer_python_test_number_easy + 1, user_id,),)
      db_tg.commit()


  #Проверка номера лёгкого вопроса по Python
  async def progress_python_test_easy_number(self, *, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      return cursor_tg.execute(
        "SELECT answer_python_test_number_easy FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
  #Возращает количество правильныхответов на лёгкие вопросы по Python
  async def enter_answer_python_test_number_easy_chek(self, *, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      return cursor_tg.execute(
        "SELECT enter_answer_python_test_number_easy FROM tg_users WHERE id = ?",
        (user_id,),
      ).fetchone()[0]
    
  #Вычетание попытки за лёгкий тест по python
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
  async def spisok_list_answer_python_test_number_easy(self, *, user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      spisok_list_answer_python_test_number_easy = cursor_tg.execute(
        "SELECT list_answer_python_test_number_easy FROM tg_users WHERE id = ?",
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
  

  




  
   

class EasyPythonTest(PythonTestBase):
  async def easy_questions_on_python_connect(self): print("Соединение с базой данных Easy_questions_on_Python.db успешно установленно!" if "Easy_questions_on_Python.db" in os.listdir("datab/Python") else "Ошибка при соединения с базой данных Easy_questions_on_Python.db!")

  #Возращает и расшифровывает вопрос по его номеру
  async def easy_questions_on_test_python(self, *, number_of_questions: int):
    with sqlite3.connect('datab/Python/Easy_questions_on_Python.db') as db:
      cursor = db.cursor()
      u = list(*cursor.execute("SELECT question, answer1, answer2, answer3, key FROM Easy_questions_on_Python WHERE number = ?", (number_of_questions,)))
      return await self.decoder(u)


    
  async def quantity_str(self):
    with sqlite3.connect('datab/Python/Easy_questions_on_Python.db') as db:
      return db.cursor().execute("SELECT COUNT(*) FROM Easy_questions_on_Python").fetchone()[0]
    






class ORM(TG_Users, EasyPythonTest):    
  def __init__(self):
    asyncio.ensure_future(self.tg_users_connect())
    asyncio.ensure_future( self.easy_questions_on_python_connect())