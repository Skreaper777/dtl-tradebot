# 1. https://metanit.com/python/database/3.3.php
# 2. https://pythonru.com/biblioteki/shemy-sqlalchemy-core
# 3. https://proglib.io/p/upravlenie-dannymi-s-pomoshchyu-python-sqlite-i-sqlalchemy-2020-10-21
# 4. https://proglib.io/p/kak-podruzhit-python-i-bazy-dannyh-sql-podrobnoe-rukovodstvo-2020-02-27

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float


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

class DB_str_n_one(Base):
    __tablename__ = "strategy_num_one"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    ticker = Column(String)
    type_signal = Column(String)
    # last_price = Column(Float)
    # update_time = Column(String)
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

class DB_str_n_two(Base):
    __tablename__ = "strategy_num_two"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    ticker = Column(String)
    type_signal = Column(String)
    level_in = Column(Float)
    last_price = Column(Float)
    update_time = Column(String)
    update_minute = Column(Integer)
    support1 = Column(Float)
    support2 = Column(Float)
    resistance1 = Column(Float)
    resistance2 = Column(Float)
    candle_x_name = Column(String)
    candle_x_value = Column(Float)
    candle_x_last_price = Column(Float)
    candle_x_time = Column(String)
    candle_x_minute = Column(Integer)
    candle_x1_name = Column(String)
    candle_x1_value = Column(Float)
    candle_x1_time = Column(String)
    candle_x1_minute = Column(Integer)
    candle_x1_last_price = Column(String)
    candle_x2_name = Column(String)
    candle_x2_value = Column(Float)
    candle_x2_time = Column(String)
    candle_x2_minute = Column(Integer)
    candle_x2_last_price = Column(String)
    pass_reason = Column(String)
    pass_reason_time = Column(String)
    pass_reason_minute = Column(Integer)
    pass_reason_value = Column(Float)
    pass_reason_last_price = Column(Float)

class DB_str_n_three(Base):
    __tablename__ = "strategy_num_three"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    ticker = Column(String)
    version = Column(Integer)
    type_signal = Column(String)
    level_in = Column(Float)
    step = Column(Float)
    max_level = Column(Integer)
    min_level = Column(Integer)
    level_in_shot = Column(Integer, default=0)
    level_in_reminder = Column(Integer, default=0)
    day_high = Column(Float)
    day_low = Column(Float)
    day_open = Column(Float)
    last_price = Column(Float)
    delta_price = Column(Float)
    update_time = Column(String)
    update_minute = Column(Integer)
    level_name = Column(String)
    level_value = Column(Float)
    support1 = Column(Float)
    support1_shot = Column(Integer, default=0)
    support1_reminder = Column(Integer, default=0)
    support2 = Column(Float)
    support2_shot = Column(Integer, default=0)
    support2_reminder = Column(Integer, default=0)
    resistance1 = Column(Float)
    resistance1_shot = Column(Integer, default=0)
    resistance1_reminder = Column(Integer, default=0)
    resistance2 = Column(Float)
    resistance2_shot = Column(Integer, default=0)
    resistance2_reminder = Column(Integer, default=0)
    candle_x0_name = Column(String)
    candle_x0_value = Column(Float)
    candle_x0_last_price = Column(Float)
    candle_x0_time = Column(String)
    candle_x0_minute = Column(Integer)
    candle_x1_name = Column(String)
    candle_x1_value = Column(Float)
    candle_x1_time = Column(String)
    candle_x1_minute = Column(Integer)
    candle_x1_last_price = Column(String)
    candle_x2_name = Column(String)
    candle_x2_value = Column(Float)
    candle_x2_time = Column(String)
    candle_x2_minute = Column(Integer)
    candle_x2_last_price = Column(String)
    pass_reason = Column(String)
    pass_reason_time = Column(String)
    pass_reason_minute = Column(Integer)
    pass_reason_value = Column(Float)
    pass_reason_last_price = Column(Float)

class DB_str_trading_simulate(Base):
    __tablename__ = "trade_simulate"

    id = Column(Integer, primary_key=True, index=True)
    create_time = Column(String)
    ticker = Column(String)
    last_price = Column(Float)
    limit_value = Column(Float)
    delta_price = Column(Float)
    date = Column(String)
    stop_loss_value = Column(Float)
    max_price = Column(Float)
    type_signal = Column(String)
    percent_win = Column(Float)
    percent_loss = Column(Float)
    type_win = Column(String)
    trade_in_time = Column(String)
    trade_in_value = Column(Float)
    trade_out_time = Column(String)
    trade_out_value = Column(Float)
    strategy_name = Column(String)
    version = Column(Integer)
    strategy_level_value = Column(Float)
    strategy_level_name = Column(String)
    time_signal = Column(String)

    update_time = Column(String)
    update_minute = Column(Integer)


class Signals(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    ticker = Column(String)
    version = Column(Integer)
    type_signal = Column(String)
    max_level = Column(Integer)
    min_level = Column(Integer)
    step = Column(Float)
    level_in = Column(Float)
    support1 = Column(Float)
    support2 = Column(Float)
    resistance1 = Column(Float)
    resistance2 = Column(Float)

class Log1(Base):
    __tablename__ = "log1"

    id = Column(Integer, primary_key=True, index=True)
    update_time = Column(String)
    # date = Column(String)
    text = Column(String)
    lvl = Column(Integer)
    date_ekb = Column(String)
    time_ekb = Column(String)
    ticker = Column(String)
    minute = Column(Integer)
    minute_tw = Column(Integer)

# def base_connecter():
#     # подключение к БД
#     # def database_connect():
#     # строка подключения
#     sqlite_database = "sqlite:///db//trades.db"
#     # sqlite_database = "sqlite:///..//trades.db"
#     # создаем движок SqlAlchemy
#     global engine
#     engine = create_engine(sqlite_database, echo=False)
#     Base.metadata.create_all(bind=engine)
#     return engine

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
        engine = create_engine(sqlite_database, echo=False)
        Base.metadata.create_all(bind=engine)
        return engine

engine = Cls_base_connecter().base_connecter()