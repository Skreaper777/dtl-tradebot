from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float


# создаем модель, объекты которой будут храниться в бд
class Base(DeclarativeBase): pass

class Cls_base_connecter:
    @staticmethod
    def base_connecter():
        # подключение к БД
        # def database_connect():
        # строка подключения
        # sqlite_database = "sqlite:/..//bot_trading//db//trades.db"
        sqlite_database = "sqlite:///..//bot_trading//db//trades.db"
        # sqlite_database = "sqlite:///..//trades.db"
        # создаем движок SqlAlchemy
        # global engine
        engine = create_engine(sqlite_database, echo=None)
        Base.metadata.create_all(bind=engine)
        return engine

class Person(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    figi = Column(String)
    ticker_name = Column(String)
    type_order = Column(String)
    open_ticker_price = Column(Float)
    time_create = Column(String)

class BaseSignals(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    type_signal = Column(String)
    level_in = Column(Float)
    support1 = Column(Float)
    support2 = Column(Float)
    resistance1 = Column(Float)
    resistance2 = Column(Float)

class DB_str_n_one(Base):
    __tablename__ = "strategy_num_one"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    ticker = Column(String)
    type_signal = Column(String)
    level_in = Column(Float)
    support1 = Column(Float)
    support2 = Column(Float)
    resistance1 = Column(Float)
    resistance2 = Column(Float)
    candle_close_1 = Column(Float)
    candle_close_2 = Column(Float)
    candle_close_3 = Column(Float)
    candle_close_4 = Column(Float)
    candle_close_5 = Column(Float)
    pass_reason = Column(String)
    last_update = Column(String)

engine = Cls_base_connecter().base_connecter()