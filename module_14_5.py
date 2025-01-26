from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions_14_5 import *
from string import ascii_letters as al


initiate_db()
prod_db()
us_db()

api = ''
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Регистрация')
button4 = KeyboardButton(text='Купить')
kb.row(button, button2)
kb.row(button3, button4)

catalog_kb = InlineKeyboardMarkup(resize_keyboard=True)
button5 = InlineKeyboardButton(text= 'Продукт 1', callback_data= 'product_buying')
button6= InlineKeyboardButton(text= 'Продукт 2', callback_data= 'product_buying')
button7 = InlineKeyboardButton(text= 'Продукт 3', callback_data= 'product_buying')
button8 = InlineKeyboardButton(text= 'Продукт 4', callback_data= 'product_buying')
catalog_kb.row(button5, button6, button7, button8)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()

    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))

    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()

@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer('Информация')

@dp.message_handler(text=['Регистрация'])
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state= RegistrationState.username)
async def set_username(message, state):
    username = message.text

    if not username.isalpha() or not all(map(lambda c: True if c in al else False, username)):
        await message.answer('Имя пользователя должно содержать только латинские буквы. Попробуйте снова.')
        return

    if is_included(username.lower()):
        await message.answer('Пользователь существует, введите другое имя.')
    else:
        await state.update_data(username=username)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()

@dp.message_handler(state= RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email = message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state= RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()

    username = data.get('username')
    email = data.get('email')
    age = int(data.get('age'))

    add_user(f'{username.lower()}', f'{email}', f'{age}')

    await message.answer('Регистрация прошла успешно')
    await state.finish()

@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    products = get_all_products()
    for product in products:
        idx, title, description, price = product
        await message.answer(f'Название: {title} | Описание: {description} | Цена: {price}')
        with open(f'files/{idx}.png', 'rb') as img:
            await message.answer_photo(img)

    await message.answer("Выберите продукт для покупки:", reply_markup=catalog_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.answer()
    await call.message.answer("Вы успешно приобрели продукт!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)
