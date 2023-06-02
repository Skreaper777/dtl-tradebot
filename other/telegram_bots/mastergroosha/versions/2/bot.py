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

# from config_reader import config
"""

1. https://metanit.com/python/database/3.3.php
2. https://pythonru.com/biblioteki/shemy-sqlalchemy-core
3. https://proglib.io/p/upravlenie-dannymi-s-pomoshchyu-python-sqlite-i-sqlalchemy-2020-10-21
4. https://proglib.io/p/kak-podruzhit-python-i-bazy-dannyh-sql-podrobnoe-rukovodstvo-2020-02-27

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float

# подключение к БД
# def database_connect():
# строка подключения
# sqlite_database = "sqlite:///db//trades.db"
sqlite_database = "sqlite:///..//..//..//..//..//bot_trading//db//trades.db"
# создаем движок SqlAlchemy
engine = create_engine(sqlite_database, echo=True)

# создаем модель, объекты которой будут храниться в бд
class Base(DeclarativeBase): pass


class Person(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    figi = Column(String)
    ticker_name = Column(String)
    type_order = Column(String)
    open_ticker_price = Column(Float)
    time_create = Column(String)


# создаем таблицы
Base.metadata.create_all(bind=engine)

bot = Bot(token="6277870580:AAE906tLUqlQOGnTlUK1eWo-WLBoTfyNPiE")
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# user_data = {}


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
# bot_trading = Bot(token="6277870580:AAGpkjQJZYL11vwzRQUsQFCxYytZ0DPPIc0")
# Диспетчер
dp = Dispatcher()


def get_keyboard_start():
    buttons = [
        [types.InlineKeyboardButton(text="Настройки бота", callback_data="setting_bot")],
        [types.InlineKeyboardButton(text="Состояние бота", callback_data="status_bot")],
        [types.InlineKeyboardButton(text="Передать информацию боту", callback_data="set_bot")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_keyboard_settings():
    buttons = [
        [types.InlineKeyboardButton(text="Задать бумаги", callback_data="setting_bot")],
        [types.InlineKeyboardButton(text="Изменить бумаги", callback_data="setting_bot")],
        [types.InlineKeyboardButton(text="Обнулить настройки", callback_data="setting_bot")]
        # [types.InlineKeyboardButton(text="Вернуться назад", callback_data="start")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



@dp.message(Command("start"))
async def cmd_numbers(message: types.Message):
    # user_data[message.from_user.id] = 0
    await message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_start())




@dp.callback_query(Text("status_bot"))
async def send_status_bot(callback: types.CallbackQuery):
    # await callback.message.answer(str(randint(1, 10)))
    await callback.answer(
        text="Бот работает исправно",
        show_alert=True
    )
    # или просто await call.answer()


@dp.callback_query(Text("setting_bot"))
async def send_setting_bot(callback: types.CallbackQuery):
    # await message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_settings())
    await callback.message.answer(str(randint(1, 10)))
    await callback.message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_settings())
    await callback.answer(
        text="Вы изменили настройки бота",
        show_alert=True
    )
    # или просто await call.answer()

@dp.callback_query(Text("set_bot"))
async def send_set_bot(callback: types.CallbackQuery):
    # await message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_settings())

    with Session(autoflush=False, bind=engine) as db:
        # создаем объект Person для добавления в бд
        tom = Person(figi="1", ticker_name="2", type_order='long',
                     open_ticker_price=777, time_create="3")
        db.add(tom)  # добавляем в бд
        db.commit()  # сохраняем изменения
    # await callback.message.answer(str(randint(1, 10)))

    # await callback.message.answer(str(randint(1, 10)))
    # await callback.message.answer("Выберите дальнейшие действие для бота", reply_markup=get_keyboard_settings())
    await callback.answer(
        text="Информация в БД отправлена",
        show_alert=True
    )
    # или просто await call.answer()




# Запуск бота
async def main():
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())