"""

https://mastergroosha.github.io/aiogram-3-guide/quickstart/#_1

"""

import asyncio
import logging

# from random import randint
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# импорты
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




# Для записей с типом Secret* необходимо
# вызывать метод get_secret_value(),
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token="6277870580:AAE906tLUqlQOGnTlUK1eWo-WLBoTfyNPiE")

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
# bot_trading = Bot(token="6277870580:AAGpkjQJZYL11vwzRQUsQFCxYytZ0DPPIc0")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Запуск бота по команде Start!")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Ведите акции, которыми хотите торговать")



@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот обновил данные в базе данных",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(Text("random_value"))
async def send_random_value(callback: types.CallbackQuery):
    with Session(autoflush=False, bind=engine) as db:
        # создаем объект Person для добавления в бд
        tom = Person(figi="1", ticker_name="2", type_order='long',
                     open_ticker_price=777, time_create="3")
        db.add(tom)  # добавляем в бд
        db.commit()  # сохраняем изменения
    # await callback.message.answer(str(randint(1, 10)))
    await callback.answer(
        text="Данные в базе данных успешно обновлены",
        show_alert=True
    )
    # await callback.answer() # или просто

if __name__ == "__main__":
    asyncio.run(main())