from aiogram import Bot,Dispatcher,types,executor
from config import token 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
import sqlite3
from datetime import datetime

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot)





database = sqlite3.connect("bot.db")
cursor = database.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INT,
    username VARCHAR (255),
    first_name VARCHAR (255),
    last_name VARCHAR (255),
    date_joined  DATETIME ); """)
database.commit()

cursor.execute ("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGERE PRIMERY KEY,
name VARCHAR(100),
title TEXT (100),
phone_number VARCHAR(100),
address_delivery VARCHAR(100)
);
                """)
database.commit()

class OrderFoodState(StatesGroup):
    name = State()
    title = State()
    phone_number = State()
    address_delivery = State()

start_buttons = [
    types.KeyboardButton("О нас"),
    types.KeyboardButton("Меню"),
    types.KeyboardButton("Адрес"),
    types.KeyboardButton("Заказать еду")
    ]

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)


@dp.message_handler(commands ="start")
async def start(message:types.Message):
    cursor.execute (f"SELECT id FROM users WHERE id = {message.from_user.id}")
    result = cursor.fetchall()
    if not result:
        cursor.execute (f"""INSERT INTO users(id,username,first_name,last_name,date_joined )
            VALUES ({message.from_user.id},
            '{message.from_user.first_name}',
            '{message.from_user.last_name}',
            '{message.from_user.username}',
            '{datetime.now()}'
            );""")

    
        await message.reply(f"Здравствуйте,{message.from_user.full_name}!Вас приветствует Ojak Kebab!",reply_markup=start_keyboard)

@dp.message_handler(text="О нас")
async def about_us(message:types.Message):
    await message.reply("Ojak Kebab - это сеть ресторанов турецкой кухни.")
    await message.answer(f"Тут вы можете узнать подробнее https://ocak.uds.app/c/about")

@dp.message_handler(text = "Меню")
async def menu_ojak(message:types.Message):
    await message.answer(f"Вот тут у нас наше меню https://nambafood.kg/ojak-kebap ")

@dp.message_handler(text="Адрес")
async def address_ojak (message:types.Message):
    await message.answer_location(42.817709,74.557861)

@dp.message_handler (text = "Заказать еду")
async def order_ojak(message:types.Message):
    await message.reply("Напишите пожалуйста Ваше имя,номер телефона и адрес доставки.")
    await OrderFoodState.name.set()


@dp.message_handler(state=OrderFoodState.name)
async def process_fodd_title(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Что хотите заказать?\n(пишите название заказа)")
    await OrderFoodState.next()

        
@dp.message_handler(state=OrderFoodState.title)
async def process_fodd_title(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await message.answer("Введите свой номер телефона")
    await OrderFoodState.next()    

@dp.message_handler(state=OrderFoodState.phone_number)
async def process_fodd_title(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.answer("Введите свой адрес: ")
    await OrderFoodState.next() 


@dp.message_handler(state=OrderFoodState.address_delivery)
async def process_fodd_title(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['address_delivery'] = message.text
    
    async with state.proxy()as data:
        name = data['name']
        title = data['title']
        phone_number = data['phone_number']
        address_delivery = data['address_delivery']
    cursor.execute ('''
INSERT INTO orders(name,title,phone_number,address_delivery)
VALUES(?,?,?,?)''',(name,title,phone_number,address_delivery))
    
    await message.answer("Ваш заказ принят!\n Курьер в пути.")
    await state.finish()

executor.start_polling(dp, skip_updates=True)
