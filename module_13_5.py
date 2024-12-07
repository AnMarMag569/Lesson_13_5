import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
bc = KeyboardButton(text="Рассчитать")
bi = KeyboardButton(text="Информация")
kb.add(bc, bi)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью. \n\n"
                         "Расчитываю по упрощенной формуле Миффлина-Сан Жеора \n"
                         "приблизительную норму калорий для женщин \n\n"
                         "Для получения информации нажмите кнопку 'Информация' \n"
                         "Для расчета нормы колорий нажмите кнопку 'Рассчитать'", reply_markup=kb)
@dp.message_handler(text='Информация')
async def set_age(message: types.Message):
    await message.answer("Упрощенная формула Миффлина-Сан Жеора ддя женщин \n"
                         "выглядит так:  10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.\n\n"
                         "Нажмите кнопку 'Рассчитать', чтобы начать расчет.", reply_markup=kb)
@dp.message_handler(text='Рассчитать')
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    calories = 10 * weight + 6.25 * growth - 5 * age - 161  # Формула для женщин

    await message.answer(f"Ваша приблизительная норма калорий: {calories}")
    await state.finish()

@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)