from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)
basicConfig(level=INFO)

start_buttons = [
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Курсы'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Контакты')
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}!", reply_markup=start_keyboard)

@dp.message_handler(text='О нас')
async def about_us(message:types.Message):
    await message.reply("Geeks - это айти курсы в Оше, Кара-Балте и Бишкеке основанная в 2019 году")

@dp.message_handler(text="Адрес")
async def send_address(message:types.Message):
    await message.answer("Наш адрес: город Ош, Мырзалы Аматова 1Б (БЦ Томирис)")
    await message.answer_location(40.51931846586533, 72.80297788183063)

@dp.message_handler(text="Контакты")
async def send_contacts(message:types.Message):
    await message.answer(f"{message.from_user.full_name} вот наши контакты")
    await message.answer_contact("+996771234213", "Ulan", "Ashirov")
    await message.answer_contact("+996777112233", "Nurbolot", "Erkinbaev")

courses = [
    types.KeyboardButton("Backend"),
    types.KeyboardButton("Frontend"),
    types.KeyboardButton("Android"),
    types.KeyboardButton("iOS"),
    types.KeyboardButton("UX/UI"),
    types.KeyboardButton("Детское программирование"),
    types.KeyboardButton("Основы программирования"),
    types.KeyboardButton("Оставить заявку", request_contact=True),
    types.KeyboardButton("Назад")
]
courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses)

@dp.message_handler(text="Курсы")
async def all_courses(message:types.Message):
    await message.answer("Вот наши курсы:", reply_markup=courses_keyboard)

@dp.message_handler(text="Backend")
async def backend(message:types.Message):
    await message.answer("Backend - это серверная стороная сайта или приложения. В осноном код вам не виден")

@dp.message_handler(text="Frontend")
async def frontend(message:types.Message):
    await message.answer("Frontend - это лицевая часть сайта или приложения. Эту часть вы можете видеть")

@dp.message_handler(text="UX/UI")
async def uxui(message:types.Message):
    await message.answer("UX/UI - это дизайн сайта или приложения")

@dp.message_handler(text="Назад")
async def back_start(message:types.Message):
    await start(message)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message:types.CallbackQuery):
    await message.answer(message)
    await bot.send_message(-4066726453, f"Заявка на курсы:\n{message.contact}")

executor.start_polling(dp)
