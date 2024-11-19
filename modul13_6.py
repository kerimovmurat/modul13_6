from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Токен бота
api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


# Inline-клавиатура
kb = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.row(button, button2)

# Клавиатура кнопок
kb1 = ReplyKeyboardMarkup(resize_keyboard=True) #  клавиатура подстраивается под размеры интерфейса устройства
button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
kb1.row(button, button2)

# Состояния пользователя
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Команда /start
@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb1)

# Текстовая команда "Рассчитать"
@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=kb)

# Callback для "Формулы расчёта"
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

# Callback для "Рассчитать норму калорий"
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

# Ввод возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

# Ввод роста
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

# Ввод веса и расчет калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    await message.answer(f"Ваша норма калорий = "
                         f"{int(10 * (data['weight']) + 6.25 *(data['growth']) - 5 *(data['age']) + 5)} ")
    await state.finish()

# Обработка прочих сообщений
@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, что бы начать общение!")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

