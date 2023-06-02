"""

https://metanit.com/python/database/3.3.php

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

# строка подключения
sqlite_database = "sqlite:///metanit.db"
# создаем движок SqlAlchemy
engine = create_engine(sqlite_database, echo=True)


# создаем модель, объекты которой будут храниться в бд
class Base(DeclarativeBase): pass


class Person(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    age2 = Column(Integer)
    money = Column(Integer)

# создаем таблицы
Base.metadata.create_all(bind=engine)

# создаем сессию подключения к бд
with Session(autoflush=False, bind=engine) as db:
    # создаем объект Person для добавления в бд
    tom = Person(name="Tom", age=40, age2=1, money=1000)
    db.add(tom)  # добавляем в бд
    db.commit()  # сохраняем изменения
    print(tom.id)  # можно получить установленный id
