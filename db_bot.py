from aiogram import Bot,Dispatcher,types,executor
from logging import basicConfig,INFO
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from config import token 
from time import ctime
import sqlite3


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
basicConfig(level=INFO)

database = sqlite3.connect('bot.db')
cursor= database.cursor()
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS users(
id INT ,
username VARCHAR (200),
first_name VARCHAR (255),
last_name VARCHAR (255),
date_joined VARCHAR(255),

               );
""")
cursor.connection.commit()



class MailingState(StatesGroup):
    message= State()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    user = cursor.execute(f"SELECT * FROM users WHERE id = {message.from_user.id}")
    result = user.fetchall()
    if result == []:
        cursor.execute("INSERT INTO users VALUES (?,?,?,?,?)",
         (message.from_user.id,message.from_user.username,
         message.from_user.first_name,message.from_user.last_name,ctime()))
        cursor.connection.commit() 
    await message.answer(f"Здравствуйте{message.from_user.full_name}")


@dp.message_handler(commands = 'mailing')
async def get_message(message:types.Message):
    await message.answer("Введите текст для рассылки:")
    await MailingState.message.set()


@dp.message_handler(state=MailingState.message)
async def send_message(message:types.Message,state:FSMContext):
    await message.answer("Начинаю рассылку")
    cursor.execute("SELECT id FROM users")
    users_id = cursor.fetchall()
    print(users_id)
    for user_id in users_id:
        await bot.send_message(user_id[0],message.text)

executor.start_polling(dp)