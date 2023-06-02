import sys
sys.path.append("C:/Users/stasr/PycharmProjects/trading-bot/venv/Lib/site-packages")

import argparse
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


parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--a", default=1, type=int, help="This is the 'a' variable", required=True)
args = parser.parse_args()


# подключение к БД
# def database_connect():
# строка подключения
# sqlite_database = "sqlite:///db//trades.db"
sqlite_database = "sqlite:///..//..//bot//db//trades.db"
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

with Session(autoflush=False, bind=engine) as db:
    # создаем объект Person для добавления в бд
    tom = Person(figi=args.a, ticker_name="2", type_order='long',
                 open_ticker_price=777, time_create="3")
    db.add(tom)  # добавляем в бд
    db.commit()  # сохраняем изменения
# await callback.message.answer(str(randint(1, 10)))