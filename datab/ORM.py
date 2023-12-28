import sqlite3
import asyncio
import os
from icecream import ic
from cryptography.fernet import Fernet
import random

class TG_Users():
  async def tg_users_connect(self):
    try:
      with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
        cursor = db_tg_users.cursor()
        query = """CREATE TABLE IF NOT EXISTS tg_users (id INTEGER, name TEXT, premium_gpt BOOLEAN, premium_test_python BOOLEAN, proba_premium_test_python INTEGER, pofil_name TEXT, user_name TEXT, answer_python_test_number_easy INTEGER, enter_answer_python_test_number_easy INTEGER, list_answer_python_test_number_easy TEXT, answer_python_test_number_medium INTEGER, enter_answer_python_test_number_medium INTEGER, list_answer_python_test_number_medium TEXT, answer_python_test_number_hard INTEGER, enter_answer_python_test_number_hard INTEGER, list_answer_python_test_number_hard TEXT)"""
        cursor.execute(query)
        print("Соединение с базой данных tg_users.db успешно создано!")
    except Exception as e:
      print(f"1Ошибка при создании таблицы в базе данных tg_users.db: {e}")

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

  async def tg_users_new_name(self, from_user):
    try:
      name = f"{from_user.first_name} {from_user.last_name}"
    except AttributeError:
      try:
        name = from_user.first_name
      except AttributeError:
        name = from_user.username
    return name

  async def tg_users_proba_id(self, from_user):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      name = cursor.execute("SELECT name FROM tg_users WHERE id = ?", (int(from_user.id),)).fetchone()
      id = cursor.execute("SELECT id FROM tg_users WHERE id = ?", (int(from_user.id),)).fetchone()
      #Ивент добавления нового пользователя в базу данных
      if id is None: 
        cursor.execute("INSERT INTO tg_users (id, proba_premium_test_python, pofil_name, user_name, premium_gpt, premium_test_python) VALUES (?, ?, ?, ?, ?, ?)", (from_user.id, 3, l := ((await asyncio.gather(self.tg_users_new_name(from_user)))[0]), from_user.username, False, False,))
        db_tg_users.commit()

      return None if (n := name) is None else n



  async def tg_users_edit_name(self, *, from_user, new_name):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      cursor.execute("UPDATE tg_users SET name = ? WHERE id = ?", (new_name, from_user.id))
      db_tg_users.commit()
      ic("Имя исправлено")

  async def tg_user_name_f_l(self, from_user): return ((await asyncio.gather(self.tg_users_new_name(from_user)))[0]) if (a := ((await asyncio.gather(self.tg_users_proba_id(from_user)))[0])) is None else a[0]
  async def tg_users_probanay_premium_test_python(self, *, from_user):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      premium_test_python = cursor.execute("SELECT premium_test_python FROM tg_users WHERE id = ?", (from_user.id,)).fetchone()
      if premium_test_python is None:
        cursor.execute("INSERT INTO tg_users (id, proba_premium_test_python, pofil_name, user_name, premium_gpt, premium_test_python, answer_python_test_number_easy, enter_answer_python_test_number_easy, list_answer_python_test_number_easy, answer_python_test_number_medium, enter_answer_python_test_number_medium, list_answer_python_test_number_medium, answer_python_test_number_hard, enter_answer_python_test_number_hard, list_answer_python_test_number_hard) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (from_user.id, 3, l := ((await asyncio.gather(self.tg_users_new_name(from_user)))[0]), from_user.username, False, False, 0, 0, '|', 0, 0, '|', 0, 0, '|',))
        return (False)
      return premium_test_python

  async def tg_users_proba_proba_premium_test_python(self, *, from_user):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      proba_premium_test_python = cursor.execute("SELECT proba_premium_test_python FROM tg_users WHERE id = ?", (from_user.id,)).fetchone()
      ic(proba_premium_test_python)
      if proba_premium_test_python is None:
        cursor.execute("INSERT INTO tg_users (id, proba_premium_test_python, pofil_name, user_name, premium_gpt, premium_test_python) VALUES (?, ?, ?, ?, ?, ?)", (from_user.id, 3, l := ((await asyncio.gather(self.tg_users_new_name(from_user)))[0]), from_user.username, False, False,))
        return (3, proba_premium_test_python)
      return proba_premium_test_python


  async def tg_users_edit_proba_premium_test_python(self, *, from_user):
    if 0 < (a := (await asyncio.gather(self.tg_users_proba_proba_premium_test_python(from_user = from_user)))[0][0]):
      a -= 1
      with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
        cursor = db_tg_users.cursor()
        cursor.execute("UPDATE tg_users SET proba_premium_test_python = ? WHERE id = ?", (a, from_user.id))
        return True
    else:
      return False



  async def tg_users_edit_premium_test_python(self, *, from_user):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      # Выполняем запрос
      cursor = db_tg_users.cursor()
      cursor.execute("UPDATE tg_users SET premium_test_python = ? WHERE id = ?", (True, from_user.id))
      # Подтверждаем изменения
      db_tg_users.commit()


  async def tg_users_edit_null(self, *, from_user):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      cursor.execute("UPDATE tg_users SET premium_test_python = ?, proba_premium_test_python = ?, premium_gpt = ? WHERE id = ?", (False, 3, False, from_user.id))
      db_tg_users.commit()
    return True
   
  async def testing_an_easy_Python_test(self, *, from_user_id: int):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor = db_tg.cursor()
      if (answer_python_test_number_easy := cursor.execute("SELECT answer_python_test_number_easy FROM tg_users WHERE id = ?", (from_user_id,)).fetchone()) is None or not answer_python_test_number_easy:
        cursor.execute("UPDATE tg_users SET answer_python_test_number_easy = ? WHERE id = ?", (0,from_user_id))
        db_tg.commit()
        answer_python_test_number_easy = 0
      ic(answer_python_test_number_easy)
      return False if 0 < answer_python_test_number_easy < 10 else True
       
  #answer_python_test_number_easy, enter_answer_python_test_number_easy, list_answer_python_test_number_easy



  async def enter_questions_easy_test_python(self, *, from_user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      answer_python_test_number_easy = cursor_tg.execute("SELECT answer_python_test_number_easy FROM tg_users WHERE id = ?", (from_user_id,)).fetchone()
      answer_python_test_number_easy = answer_python_test_number_easy[0] + 1
      cursor_tg.execute("UPDATE tg_users SET answer_python_test_number_easy = ? WHERE id = ?", (answer_python_test_number_easy, from_user_id,))
      db_tg.commit()

  async def list_answer_python_test_number_easy(self, *, from_user_id, number):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg:
      cursor_tg = db_tg.cursor()
      list_answer_python_test_number_easy = cursor_tg.execute(
        "SELECT list_answer_python_test_number_easy FROM tg_users WHERE id = ?",
        (from_user_id,),
      ).fetchone()
      list_answer_python_test_number_easy = list_answer_python_test_number_easy[0] if list_answer_python_test_number_easy else ""
      list_answer_python_test_number_easy = f"{list_answer_python_test_number_easy}{number}"
      cursor_tg.execute(
        "UPDATE tg_users SET answer_python_test_number_easy = ? WHERE id = ?",
        (list_answer_python_test_number_easy, from_user_id,),
      )
      db_tg.commit()





  async def all_easy_python_test_delete_null(self, *, from_user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      cursor.execute("UPDATE tg_users SET answer_python_test_number_easy = ?, enter_answer_python_test_number_easy = ?, list_answer_python_test_number_easy = ? WHERE id = ?", (0, 0, "|", from_user_id))
      db_tg_users.commit()

  async def progress_python_test_easy(self, *, from_user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor_tg = db_tg_users.cursor()
      answer_python_test_number_easy_or_enter_answer_python_test_number_easy = cursor_tg.execute(
        "SELECT answer_python_test_number_easy , enter_answer_python_test_number_easy FROM tg_users WHERE id = ?",
        (from_user_id,),
      ).fetchone()
      if answer_python_test_number_easy_or_enter_answer_python_test_number_easy is None:
        await self.all_easy_python_test_delete_null(from_user_id=from_user_id)
        answer_python_test_number_easy_or_enter_answer_python_test_number_easy = [0, 0]
      answer_python_test_number_easy = answer_python_test_number_easy_or_enter_answer_python_test_number_easy[0]
      enter_answer_python_test_number_easy = answer_python_test_number_easy_or_enter_answer_python_test_number_easy[1]
      return f"""
      Всего заданий выполнено: {answer_python_test_number_easy}/{10}
      Правильно выполнено: {enter_answer_python_test_number_easy}/{answer_python_test_number_easy}
      """



  async def progress_python_test_easy_number_ex_edit(self, *, from_user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor_tg = db_tg_users.cursor()

      answer_python_test_number_easy = cursor_tg.execute(
        "SELECT answer_python_test_number_easy FROM tg_users WHERE id = ?",
        (from_user_id,),
      ).fetchone()

      if answer_python_test_number_easy < 10:
        answer_python_test_number_easy += 1
      else:
        answer_python_test_number_easy = 0
      cursor_tg.execute(
        "UPDATE tg_users SET answer_python_test_number_easy = ? WHERE id = ?",
        (answer_python_test_number_easy, from_user_id,),
      )
      db_tg_users.commit()
      return answer_python_test_number_easy

  async def enter_answer_python_test_number_easy_chek(self, *, from_user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      return cursor.execute("SELECT enter_answer_python_test_number_easy FROM tg_users WHERE id = ?", (from_user_id,)).fetchone()

  async def answer_python_test_number_easy_chek(self, *, from_user_id):
    with sqlite3.connect('datab/TG/tg_users.db') as db_tg_users:
      cursor = db_tg_users.cursor()
      answer_number = cursor.execute("SELECT answer_python_test_number_easy FROM tg_users WHERE id = ?", (from_user_id,)).fetchone()

      if answer_number is None:
        answer_number = 0

      return answer_number

  



#id=1976113730, is_bot=False, first_name='Влад', last_name='Санин', username='Vlad_sanin_777', language_code='ru', is_premium=None, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None

class PythonTestBase():
  async def decoder(self, question: list):
    ic("Декодер работает!")
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


  async def easy_questions_on_test_python(self, *, number_of_questions: int):
    ic(number_of_questions)
    with sqlite3.connect('datab/Python/Easy_questions_on_Python.db') as db:
      cursor = db.cursor()
      ic(cursor)
      u = list(*cursor.execute("SELECT question, answer1, answer2, answer3, key FROM Easy_questions_on_Python WHERE number = ?", (number_of_questions,)))

      ic(u)
      #value = []
      # Convert generator to awaitable task
      #for decoded_question in await asyncio.ensure_future(self.decoder(u)):
        #value.append(decoded_question)
      return await self.decoder(u)


    
  async def quantity_str(self):
    with sqlite3.connect('datab/Python/Easy_questions_on_Python.db') as db:
      return db.cursor().execute("SELECT COUNT(*) FROM Easy_questions_on_Python").fetchone()[0]




class ORM(TG_Users, EasyPythonTest):    
  def __init__(self):
    asyncio.ensure_future(self.tg_users_connect())
    asyncio.ensure_future( self.easy_questions_on_python_connect())