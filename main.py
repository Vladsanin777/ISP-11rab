import os
import asyncio
from typing import Optional

import aiogram
from aiogram import Bot, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

import disnake
from disnake.ext import commands

from openai import AsyncOpenAI

from typing import Optional


import cogs.new

import dataclasses
from dataclasses import dataclass

import random

import cogs.raspisanie_day

import element.gpt

import element.dover_isp
import math

import cogs.nedelay
import cogs.stabil

import datetime

import sqlite3

from datab.ORM import ORM, EasyPythonTest, TG_Users

from icecream import ic

from cryptography.fernet import Fernet

import TOKEN

class Code():
    async def generator_key(self):
        return Fernet.generate_key()

    async def encode_1(self, *, value):
        key = await self.generator_key()  # Generate key before encryption
        value_bytes = value.encode()  # Encode text to bytes before encryption
        return Fernet(key).encrypt(value_bytes), key

    async def decode_1(self, *, value, key):
        #value_bytes = value.encode()  # Encode text to bytes before decryption
        return Fernet(key).decrypt(value).decode()  # Decode result back to text

  
async def main_2():
    run = input("Введите действие: ")
    match run:
        case "-en":
            value_to_encrypt = input("Текст который надо зашивровать: ")
            value, key = await Code().encode_1(value=value_to_encrypt)
            print(f"Зашифрованный текст: {value}\nКлюч: {key.decode()}")  # Decode key for display
        case "-de":
            value_to_decrypt = input("Текст который надо расзашивровать: ")
            key = input("Введите ключь для расшифровки: ").encode()  # Encode key before decryption
            print(await Code().decode_1(value=value_to_decrypt, key=key))
        case _:
            print("Такого действия нет")




# Инициализируем бота Discord
intents = disnake.Intents.default()
intents.message_content = True  # Добавить эту строку

bot = commands.Bot(command_prefix='!', intents=intents)


# Инициализируем бота Telegram


dp = aiogram.Dispatcher()


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            yui = f"cogs.{filename[:-3]}"
            try:
                bot.load_extension(yui)
            except BaseException:
                print(f"Не удалось загрузить {yui}")


@bot.event
async def on_ready():
    print(f'Дискорд бот {bot.user} полностью загрузился')
    #asyncio.ensure_future(cogs.stabil.Stabil(bot).stabil())
    #asyncio.ensure_future(cogs.nedelay.Nedelay(bot).nedelay_loop())

    #asyncio.ensure_future(cogs.raspisanie_day.Raspisanie(bot).raspisanie_loop())

@dp.message(CommandStart())
async def command_start_handler(message: aiogram.types.Message) -> None:
    await message.delete()
    if (await TG_Users().tg_user_poverka_new_user(id_tg = message.from_user.id))[0] is None:
        await TG_Users().tg_users_edit_all_newuser(id = message.from_user.id, pofil_name = (await TG_Users().tg_users_new_name(message.from_user)), user_name = message.from_user.username, name = (name := (await TG_Users().tg_users_new_name(from_user = message.from_user))[0][0]))
    else:
        name = await TG_Users().tg_users_name(from_user = message.from_user)[0][0][0] if (n := await TG_Users().tg_users_proba_name(id_tg = message.from_user.id))[0][0][0] is None else n
    button1 = InlineKeyboardButton(text="Закрыть", callback_data='esc')
    catalog_list = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    await message.answer(f'Привет, {name}\nУ меня есть следующие комманды:\n/start - для получения информации о боте\n/gpt - для взоимодействия с ChatGPT 3.5\n/new - для отправки новости всей группе\n/promo - для получения возможностей\n/help - для обращения в техподдержку бота\n/info - полный список команд\n/name - изменить обращение к вам\n/python_test', reply_markup = catalog_list)

@dp.message(Command(commands = ["name"]))
async def edit_name(message: aiogram.types.Message):
    await message.delete()
    button1 = InlineKeyboardButton(text="Закрыть", callback_data='esc')
    catalog_list = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    name = ((await asyncio.gather(TG_Users().tg_users_proba_id(message.from_user)))[0])
    new_name = ''.join((message.text[6:]).split())
    if not(new_name.isalpha()):
        new_name = None
    if name is None and new_name is None:
        await message.answer('Вы не ввели имя по которому я вас смогу к вам обращаться по этому я продолжу обращаться к вам по профилю Telegram.\nЕсли это вас не устраивает то введите:\n/name - и своё имя', reply_markup = catalog_list)
    elif name is None :
        await asyncio.gather(TG_Users().tg_users_edit_name(from_user = message.from_user, new_name = new_name))
        await message.answer(f"Теперь я буду обращеться к тебе {new_name}", reply_markup = catalog_list)
    elif new_name is None:
        await asyncio.gather(TG_Users().tg_users_edit_name(from_user = message.from_user, new_name = None))
        await message.answer(f'Теперь я буду обращеться к тебе по профилю, а не {name[0]}', reply_markup = catalog_list)
    else:
        await asyncio.gather(TG_Users().tg_users_edit_name(from_user = message.from_user, new_name = new_name))
        await message.answer(f'Старое имя {name[0]}\nНовое имя {new_name}', reply_markup = catalog_list)








@dp.message(Command(commands=["help"]))
async def help_command(message: aiogram.types.Message):
    await message.delete()
    message_tg_help = f'У пользователя {message.from_user.first_name} {message.from_user.last_name}\n id {message.from_user.id} \n {message.from_user.username} есть какое то обращение к тебе\n{message.text}'
    await bot_t.send_message(chat_id=1976113730, text=message_tg_help)
    await message.answer(
        f'Привет, {message.from_user.first_name} {message.from_user.last_name}\nТы обратился к разработчику бота вот твоё обращение:\n{message_tg_help}'
    )




@dataclass
class UserConfirmation:
    user_id: int
    confirmation_count: int = 0
    message_tg: str = "Введите ваш вопрос"

user_confirmations = {}  # Словарь для хранения объектов UserConfirmation

async def find_key(value, dictionary):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

# Обработчик для команды '/new'
@dp.message(Command(commands=["new"]))
async def new(message: aiogram.types.Message) -> None:
    await message.delete()
    if message.from_user.id in element.dover_isp.DoverISP().tg_enter_class_s or message.from_user.id in dover_isp.DoverISP().tg_enter_class.values():
        if message.from_user.id in element.dover_isp.DoverISP().tg_enter_class_s:
            message_tg = f"Новость отправлена из Telegram\nИз чата: {message.chat.first_name}\nC id {message.chat.id}\nПользователем: {message.from_user.first_name} {message.from_user.last_name}\nС именем пользователя {message.from_user.username}\nid данного пользователя в телеграмм{message.from_user.id}\nДанный пользователь не является оффицальным\nНовость: {message.text[5:]}"
        elif message.from_user.id in element.dover_isp.DoverISP().tg_enter_class.values():


            message_tg = f"Новость отправлена из Telegram\nИз чата: {message.chat.first_name}\nC id {message.chat.id}\nПользователем: {message.from_user.first_name} {message.from_user.last_name}\nС именем пользователя {message.from_user.username}\nid данного пользователя в телеграмм{message.from_user.id}\nДанный пользователь является оффициальным {(await asyncio.gather(find_key(message.from_user.id, dover_isp.DoverISP().tg_enter_class)))[0]}\nНовость: {message.text[5:]}"
        button1 = InlineKeyboardButton(text="Подтвердить", callback_data='confirm')
        button2 = InlineKeyboardButton(text="Отменить", callback_data='cancel')
        catalog_list = InlineKeyboardMarkup(inline_keyboard=[[button1, button2]])
        await message.answer(f"Подтвердите отправку новости:\n{message_tg}", reply_markup=catalog_list)

        # Создаем объект UserConfirmation для пользователя, если его еще нет
        user_id = message.from_user.id
        confirmation_count = 0

        user_confirmations[user_id] = UserConfirmation(user_id)
        user_id = message.from_user.id
        user_confirmation = user_confirmations.get(user_id)
        user_confirmation.confirmation_count = 0
        user_confirmation.message_tg = message_tg
    else:
        await message.answer(f"Вам недоступна данная команда")

# Обработчик для callback_data 'confirm'
@dp.callback_query(lambda query: query.data == 'confirm')
async def confirm_button_handler_1(query: aiogram.types.CallbackQuery):
    # Получаем объект UserConfirmation для пользователя
    user_id = query.from_user.id
    user_confirmation = user_confirmations.get(user_id)

    # Проверяем, что пользователь еще не подтверждал новость дважды
    if user_confirmation and user_confirmation.confirmation_count < 2:
        # Увеличиваем счетчик подтверждений для данного пользователя
        user_confirmation.confirmation_count += 1

        if user_confirmation.confirmation_count == 2:
            # Если пользователь подтвердил два раза, отправляем исходный текст новости
            await query.message.delete()
            await query.message.answer(f'✔ Отправка подтверждена! {user_confirmation.message_tg}')
            await asyncio.gather(cogs.new.new(bot).is_tg_in_ds(user_confirmation.message_tg))
            for chat in element.dover_isp.DoverISP().tg_enter_class_send.values():
                if chat != query.message.chat.id:
                    await bot_t.send_message(chat_id=1976113730, text=user_confirmation.message_tg)
                else:
                    pass
            else:
                # Отправляем запрос на подтверждение второго раза
                button1 = InlineKeyboardButton(text="Нет", callback_data='cancel')
                button2 = InlineKeyboardButton(text="Да", callback_data='confirm')
                catalog_list = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])
                await query.message.delete()
                await query.message.answer(text = f'Вы уверены?\nПодтвердите отправку новости:\n{user_confirmation.message_tg}', reply_markup=catalog_list)



# Обработчик для callback_data 'cancel'
@dp.callback_query(lambda query: query.data == 'cancel')
async def confirm_button_handler_2(query: aiogram.types.CallbackQuery):
    await query.message.delete()
    button1 = InlineKeyboardButton(text="Закрыть", callback_data='esc')
    catalog_list = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    user_id = query.from_user.id
    user_confirmation = user_confirmations.get(user_id)
    await query.message.answer(text = f'❌ Отправка отменина.\nВы отменили данную отправку:\n{user_confirmation.message_tg}', reply_markup=catalog_list)



@dp.callback_query(lambda query: query.data == 'esc')
async def confirm_button_handler_0(query: aiogram.types.CallbackQuery):
    await query.message.delete()



@dp.message(Command(commands=["gpt"]))
async def gpt_command(message: aiogram.types.Message):
    await message.delete()
    button1 = InlineKeyboardButton(text="Закрыть", callback_data='esc')
    catalog_list = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    if message.from_user.id in element.dover_isp.DoverISP().gpt_tg or message.from_user.id in element.dover_isp.DoverISP().tg_enter_class_s or message.from_user.id in element.dover_isp.DoverISP().tg_enter_class.values():
        enter_dostyp = True
    else:
        enter_dostyp = False
        await message.answer("напишите /promo ПАРОЛЬ КОТОРЫЙ ВАМ ДАЛ РАЗРАБОТЧИК БОТА для этой функции", reply_markup=catalog_list)
    match enter_dostyp:
        case True:
            message_gpt = len(message.text)
            match message_gpt:
                case 4:
                    await message.answer('Gpt не сможет ответить на пустой текст', reply_markup=catalog_list)
                case _:
                    message_gpt = message.text[5:]
                    if message_gpt != "" and message_gpt != None and message_gpt != " ":
                        await message.answer(f'Сейчас GPT ответит на вопрос: {message_gpt}', reply_markup=catalog_list)
                        response_gpt = await asyncio.gather(element.gpt.gpt().gpt(message_gpt, 4000))
                        print(response_gpt[0])
                        for i in response_gpt[0]:
                            await message.answer(text = i)
                    else:
                        await message.answer('Gpt не сможет ответить на пустой текст', reply_markup=catalog_list)





@dp.message(Command(commands=["promo"]))
async def promo(message: aiogram.types.Message):
    await message.delete()
    message_tg = message.text[7:]
    if len(element.dover_isp.DoverISP().gpt_tg) >= 150:
        element.dover_isp.DoverISP().gpt_tg.clear()
    button1 = InlineKeyboardButton(text="Закрыть", callback_data='esc')
    catalog_list = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    if message_tg == element.dover_isp.DoverISP( ).tg_enter_class_pashword:
        await message.answer(f"Вы активировали перемиум на всё и {await TG_Users().promo_all_tg_bd(message.from_user.id)}", reply_markup=catalog_list)
    else:
        await message.answer(f"Вы ввели не существующий промокод!", reply_markup=catalog_list)
        





@dp.message(Command(commands=["info"]))
async def info(message: aiogram.types.Message) -> None:
    await message.delete()
    await message.answer(f"Все мои коммады:\n/start - для получения информации о боте\n/gpt - для взоимодействия с ChatGPT 3.5\n/new - для отправки новости всей группе\n/promo - для получения возможностей\n/help - для обращения в техподдержку бота\n/info - полный список команд\n/nod - для поиска нода\n/nok - для поиска нока\n/name - изменить обращение к вам\n/python_test")

class BaseViewTG():
    def __init__(self):
        self.esc = InlineKeyboardButton(text="Закрыть", callback_data="esc")
        self.keyboard_esc = InlineKeyboardMarkup(inline_keyboard = [[self.esc]])
        self.test_python_pause_enter_easy = InlineKeyboardButton(text="Да, хочу продолжить лёгкий тест!", callback_data="test_python_pause_enter_easy")
        self.test_python_pause_not_enter_easy = InlineKeyboardButton(text="Нет, я хочу начать лёгкий тест сначала", callback_data="test_python_pause_not_enter_easy")
        self.keyboard_python_test_easy = InlineKeyboardMarkup(inline_keyboard = [[self.test_python_pause_not_enter_easy], [self.test_python_pause_enter_easy], [self.esc]])

class PythonTestViewTG(BaseViewTG):
    def __init__(self):
        self.hard = InlineKeyboardButton(text="Сложный", callback_data="hard_python_test")
        self.medium = InlineKeyboardButton(text="Средний", callback_data="medium_python_test")
        self.easy = InlineKeyboardButton(text="Лёгкий", callback_data="easy_python_test")
        self.keyboard = InlineKeyboardMarkup(inline_keyboard = [[self.easy], [self.medium], [self.hard], [BaseViewTG().esc]])
    




@dp.message(Command(commands=["python_test"]))
async def python_test(message: aiogram.types.Message) -> None:
    await message.delete()
    pt = PythonTestViewTG()
    warning, text, access = await TG_Users().tg_users_proba_and_premium_test_python(user_id = message.from_user.id)
    if access:
        if warning:
            await message.answer(f"{text}\nВы действительно хотите потратить одну попытку сейчас?", reply_markup = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text="Да", callback_data="python_test_yes"), BaseViewTG().esc]]))
        else:
            await message.answer(f"Если хотите пройти тест по python, то выбирите уровень сложности или закрыть если передумали:", reply_markup = pt.keyboard)
    else:
        await message.answer("У вас закончились попытки и нет премиума!", reply_markup = BaseViewTG().keyboard_esc)

@dp.callback_query(lambda query: query.data == 'python_test_yes')
async def python_test_yes(query: aiogram.types.CallbackQuery):
    await query.message.delete()
    pt = PythonTestViewTG()
    await query.message.answer(f"Если хотите пройти тест по python, то выбирите уровень сложности или закрыть если передумали:", reply_markup = pt.keyboard)


async def to_nested_list(list_to_convert):
    if not list_to_convert:
        return []
    
    return [[item] for item in list_to_convert]


#Отправляет лёгкий вопрос по Python
async def generator_question_easy(*, query):
    random_question = None
    count_question = await EasyPythonTest().quantity_str()
    spisok_using_question = await TG_Users().spisok_list_answer_python_test_number_easy(user_id = query.from_user.id)
    while True:
        random_question = random.randint(1, count_question)
        if count_question < len(spisok_using_question) or str(random_question) not in spisok_using_question:
            break
    answer_question = await EasyPythonTest().easy_questions_on_test_python(number_of_questions = random_question)    
    answer = answer_question.copy()[1:]
    random.shuffle(answer)
    buttons = []
    for i in answer:
        p = i if i[0] != "~" else i[1:]
        ans = "not_enter_questions_easy_test_python" if p is i else "enter_questions_easy_test_python"
        buttons.append(InlineKeyboardButton(text=p, callback_data=ans))

    inline_keyboard = [[button] for button in buttons]
    inline_keyboard.append([InlineKeyboardButton(text="Закрыть", callback_data="esc")])
    await TG_Users().list_answer_python_test_number_easy(user_id = query.from_user.id, number = random_question)
    await query.message.answer(f"{await TG_Users().progress_python_test_easy(user_id = query.from_user.id)}\nВопрос №{(await TG_Users().answer_python_test_number_easy_chek(user_id = query.from_user.id)) + 1}\n{answer_question[0]}", reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
  
#Выдаёт пользователю результат прохождения лёгкого теста по python или задаёт следующий вопрос
async def end_test_python_easy(*, query):
    if (await TG_Users().progress_python_test_easy_number(user_id = query.from_user.id)) < 10:
        await generator_question_easy(query=query)
    else: 
        await query.message.answer(f"Вы прошли ЛЁГКИЙ ТЕСТ по Python:\nВаш результат {await TG_Users().enter_answer_python_test_number_easy_chek(user_id = query.from_user.id)}/10",reply_martkup = BaseViewTG().keyboard_esc)
        await TG_Users().all_easy_python_test_delete_null(user_id = query.from_user.id)

#Вызывается при неправильном ответе на лёгкий вопрос по Python
@dp.callback_query(lambda query: query.data == 'not_enter_questions_easy_test_python')
async def not_enter_questions_easy_test_python(query: aiogram.types.CallbackQuery) -> None:
    await query.message.delete()
    await TG_Users().not_enter_questions_easy_test_python(user_id = query.from_user.id)
    await end_test_python_easy(query=query)


#Вызывается при правильном ответе на лёгкий вопрос по Python
@dp.callback_query(lambda query: query.data == 'enter_questions_easy_test_python')
async def enter_questions_easy_test_python(query: aiogram.types.CallbackQuery) -> None:
    await query.message.delete()
    await TG_Users().enter_questions_easy_test_python(user_id = query.from_user.id)
    await end_test_python_easy(query=query)
    
  
    
  

#Вызывается для обнуления сеанса лёгкого теста по пайтону и вызова нового сеанса тестирования
@dp.callback_query(lambda query: query.data == 'test_python_pause_not_enter_easy')
async def test_python_pause_not_enter_easy(query: aiogram.types.CallbackQuery) -> None:
    try: await query.message.delete()
    except: pass
    await TG_Users().edit_proba_premium_test_python(user_id = query.from_user.id)
    await TG_Users().all_easy_python_test_delete_null(user_id = query.from_user.id)
    await generator_question_easy(query = query)


#Вызывается для Продалжения сеанса лёгкого теста по пайтону
@dp.callback_query(lambda query: query.data == 'test_python_pause_enter_easy')
async def test_python_pause_enter_easy(query: aiogram.types.CallbackQuery) -> None:
    try: await query.message.delete()
    except: pass
    await generator_question_easy(query = query)

#Проверка предидущего сеанса лёгкого теста по пайтону
@dp.callback_query(lambda query: query.data == 'easy_python_test')
async def easy_python_test(query: aiogram.types.CallbackQuery) -> None:
    await query.message.delete()
    if (await TG_Users().testing_an_easy_Python_test(user_id = query.from_user.id)) != 0:
        await query.message.answer(f"Хотите продолжить лёгкое тестирование по Python с сохранением попытки или начать с начало!\n{await TG_Users().progress_python_test_easy(user_id = query.from_user.id)}", reply_markup = BaseViewTG().keyboard_python_test_easy)
    else:
        await TG_Users().edit_proba_premium_test_python(user_id = query.from_user.id)
        await test_python_pause_not_enter_easy(query = query)



@dp.message(Command(commands=["n"]))
async def n(message: aiogram.types.Message) -> None:
    await message.delete()
    button1 = InlineKeyboardButton(text="Закрыть", callback_data='esc')
    catalog_list = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    if message.from_user.id == 1976113730:
        await asyncio.gather(TG_Users().user_null(user_id = message.from_user.id))
        await message.answer("Ваш акаунт обнулён!", reply_markup=catalog_list)
    else: await message.answer("Снос акаунта не возможен!\nПотому что вы не являетесь тестировщиком и разработчиком бота!", reply_markup=catalog_list)

@dp.message(Command(commands=["nod"]))
async def nod_command(message: aiogram.types.Message) -> None:
    await message.delete()
    await message.answer(f"НОД всех этих чисел:\n{message.text[5:]}\nРавно: {math.gcd(*map(int, message.text[5:].split(', ')))}")

@dp.message(Command(commands=["nok"]))
async def nok_command(message: aiogram.types.Message) -> None:
    await message.delete()
    await message.answer(f"НОК всех этих чисел: {message.text[5:]}\nРавно: {math.lcm(*map(int, message.text[5:].split(', ')))}")


@dp.message(Command(commands=["log"]))
async def log_command(message: aiogram.types.Message) -> None:
    await message.delete()
    arg = message.text[5:].split(", ")
    result = math.log(int(arg[1]), int(arg[0]))
    await message.answer(f"log с основанием {arg[0]}:\nЧисела: {arg[1]}\nРавняется: {result}")

@dp.message(Command(commands=["lg"]))
async def lg_command(message: aiogram.types.Message) -> None:
    await message.delete()
    arg = message.text[5:].split(", ")
    result = math.log10(int(arg[0]))
    await message.answer(f"lg или log с основанием 10:\nЧисела: {arg[0]}\nРавняется: {result}")

@dp.message(Command(commands=["lb"]))
async def lb_command(message: aiogram.types.Message) -> None:
    await message.delete()
    arg = message.text[5:].split(", ")
    result = math.log2(int(arg[0]))
    await message.answer(f"lb или log с основанием 2:\nЧисела: {arg[0]}\nРавняется: {result}")

@dp.message(Command(commands=["ln"]))
async def ln_command(message: aiogram.types.Message) -> None:
    await message.delete()
    arg = message.text[5:].split(", ")
    result = math.log1p(int(arg[0]))
    await message.answer(f"ln или log с основанием числа e = {math.e}:\nЧисела: {arg[0]}\nРавняется: {result}")




async def main_5():
    # Создать ORM
    ORM()

    # Декодировать токены
    ds = await Code().decode_1(value = TOKEN.DS_token[0], key = TOKEN.DS_token[1])
    tg = await Code().decode_1(value = TOKEN.TG_token[0], key = TOKEN.TG_token[1])

    # Инициализировать ботов
    tasks = [
        asyncio.ensure_future(dp.start_polling(aiogram.Bot(token=tg))),
        asyncio.ensure_future(bot.start(ds)),
    ]

    # Запустить задачи
    await asyncio.gather(*tasks)


# Запустить цикл событий
asyncio.run(main_5())


