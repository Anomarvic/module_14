from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
# from pymunk.examples.newtons_cradle import description
from crud_functions import *

initiate_db()
prod_db()

api = '7917373357:AAHnfoU5ZrSqtmlbx0iEWwMAon_aDQZ7rfU'
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.row(button, button2)
kb.add(button3)

catalog_kb = InlineKeyboardMarkup(resize_keyboard=True)
button4 = InlineKeyboardButton(text= 'Продукт 1', callback_data= 'product_buying')
button5 = InlineKeyboardButton(text= 'Продукт 2', callback_data= 'product_buying')
button6 = InlineKeyboardButton(text= 'Продукт 3', callback_data= 'product_buying')
button7 = InlineKeyboardButton(text= 'Продукт 4', callback_data= 'product_buying')
catalog_kb.row(button4, button5, button6, button7)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

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