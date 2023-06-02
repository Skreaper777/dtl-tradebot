from aiogram import types, Bot, Dispatcher
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
from aiogram.fsm.context import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FSM storage
memory_storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token="6277870580:AAE906tLUqlQOGnTlUK1eWo-WLBoTfyNPiE")
dp = Dispatcher(storage=memory_storage)

# bot = Bot(token="6277870580:AAE906tLUqlQOGnTlUK1eWo-WLBoTfyNPiE")
# dp = Dispatcher()

class InputUserData(StatesGroup):
    step_1 = State()

@dp.message_handler(commands=['start'])
async def startpg(message: types.Message, state: FSMContext):
    keyboard_markup = types.InlineKeyboardMarkup()
    button9 = types.InlineKeyboardButton('button9', callback_data = 'button9')
    keyboard_markup.row(button9)
    await message.reply('Добро пожаловать!\nЭто бот тестер, нажмите на Inline кнопку ниже', reply_markup=keyboard_markup)

@dp.callback_query_handler(lambda c: c.data == 'button9')
async def handle_a(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Введите значение переменной a:')
    await InputUserData.step_1.set()

@dp.message_handler(state=InputUserData.step_1, content_types=types.ContentTypes.TEXT)
async def questionnaire_state_1_message(message: types.Message, state: FSMContext):
    async with state.proxy() as user_data:
    # Здесь user_data является хранилищем (а точнее словарем), куда можно сохранять определенные данные и вытаскивать если нужно в любой момент
        user_data['input_user'] = message.text.replace('\n',' ') # Вы возможно спросите - для чего нужен здесь replace, он нужен в случае если юзер умудрится написать значение переменной a на двух строках, у меня на практике такое было несколько раз

    a = user_data['input_user']

    await message.reply(f"Значение переменной a: {a}")

    await state.finish() # Оканчиваем наш FSM опрос от пользывателя

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)