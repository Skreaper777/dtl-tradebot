
import asyncio
import logging
from contextlib import suppress
from random import randint
from typing import Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Text, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# сlass Form(StatesGroup):
#     peremennaya = State() # Задаем состояние
#
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await bot.send_message(message.chat.id, 'Отправь свое сообщение:')
#     await Form.peremennaya.set() # Устанавливаем состояние
#
# @dp.message_handler(state=Form.a) # Принимаем состояние
# async def start(message: types.Message, state: FSMContext):
#     async with state.proxy() as proxy: # Устанавливаем состояние ожидания
#     a['peremennaya'] = message.text
#     await state.finish() # Выключаем состояние