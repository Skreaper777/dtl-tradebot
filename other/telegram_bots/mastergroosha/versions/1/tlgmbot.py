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
bot = Bot(token="6277870580:AAHcSw-j9HVSXtC0Z0cYSQK9YyHLm5rcubU")

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
    dp.message.register(cmd_test2, Command("test2"))

    await dp.start_polling(bot)

# Хэндлер на команду /test1
@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")

# Хэндлер на команду /test2
async def cmd_test2(message: types.Message):
    await message.reply("Test 2")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="С пюрешкой"),
            types.KeyboardButton(text="Без пюрешки")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

@dp.message(Text("С пюрешкой"))
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!")

@dp.message(lambda message: message.text == "Без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")

@dp.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text="Запросить геолокацию", request_location=True),
        types.KeyboardButton(text="Запросить контакт", request_contact=True)
    )
    # ... второй из одной ...
    builder.row(types.KeyboardButton(
        text="Создать викторину",
        request_poll=types.KeyboardButtonPollType(type="quiz"))
    )
    # ... а третий снова из двух
    builder.row(
        types.KeyboardButton(
            text="Выбрать премиум пользователя",
            request_user=types.KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True
            )
        ),
        types.KeyboardButton(
            text="Выбрать супергруппу с форумами",
            request_chat=types.KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )
    )
    # WebApp-ов пока нет, сорри :(

    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

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
    await callback.answer() # или просто

if __name__ == "__main__":
    asyncio.run(main())