from sqlalchemy import create_engine, update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.sql.expression import bindparam

# from bot_telegram.lib.dbcommon import BaseSignals, Person, engine
from bot_trading.lib.db.db_main import DB_str_n_one, DB_str_n_two, DB_str_n_three, Signals, engine

def base_upload_signals_base(global_query_lst):
    for data in global_query_lst:
        # print(1111, data)
        with Session(autoflush=False, bind=engine) as db:
            tom = Signals(**data)
            db.add(tom)  # добавляем в бд
            db.commit()  # сохраняем изменения

def base_upload_signals_to_strategies(global_query_lst, version=None):
    for data in global_query_lst:
        # print(1111, data)
        # with Session(autoflush=False, bind=engine) as db:
        #     tom = Signals(**data)
        #     db.add(tom)  # добавляем в бд
        #     db.commit()  # сохраняем изменения

        with Session(autoflush=False, bind=engine) as db:
            # qs_num_one = db.query(DB_str_n_one).filter(DB_str_n_one.ticker == data["ticker"], DB_str_n_one.date == data["date"]).first()
            # qs_num_two = db.query(DB_str_n_two).filter(DB_str_n_two.ticker == data["ticker"],
            #                                            DB_str_n_two.date == data["date"]).first()
            qs_num_three = db.query(DB_str_n_three).filter(DB_str_n_three.ticker == data["ticker"],
                                                       DB_str_n_three.date == data["date"],
                                                       DB_str_n_three.version == version
                                                           ).first()

        # if qs_num_one!=None:
        #     # qs_num_one.type_signal = data.get("type_signal", None)
        #     # qs_num_one.level_in = data.get("level_in", None)
        #     # qs_num_one.support1 = data.get("support1", None)
        #     # qs_num_one.support2 = data.get("support2", None)
        #     # qs_num_one.resistance1 = data.get("resistance1", None)
        #     # qs_num_one.resistance2 = data.get("resistance2", None)
        #     #
        #     # db.add(qs_num_one)
        #     # db.commit()
        #     db.delete(qs_num_one)
        # if qs_num_two != None:
        #     db.delete(qs_num_two)
        if qs_num_three != None:
            db.delete(qs_num_three)
        # else:

        # tom = DB_str_n_one(**data)
        # tom2 = DB_str_n_two(**data)

        # Добавлем версию стратегии
        data["version"] = version

        tom3 = DB_str_n_three(**data)
        # db.add(tom)  # добавляем в бд
        # db.add(tom2)  # добавляем в бд
        db.add(tom3)  # добавляем в бд
        db.commit()  # сохраняем изменения



    # Если в таблице стратегии еще не создана строка с тикером, то создать ее
    # if not self.qs_num_one:
    #     with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
    #         # print(db.query(dbmain.Signals).filter(dbmain.Signals.ticker == ticker).first().__dict__)
    #         query_signals = db.query(dbmain.Signals).filter(dbmain.Signals.ticker == self.ticker).first()
    #
    #     level_in = query_signals.level_in
    #     with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
    #         query = dbmain.DB_str_n_one(ticker=self.ticker, level_in=level_in, type_signal=query_signals.type_signal, last_update=utl.Utility.current_utc_time())
    #         db.add(query)
    #         db.commit()
    #     # выборка текущего тикера из таблицы стратегии
    #     with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
    #         self.qs_num_one = db.query(dbmain.DB_str_n_one).filter(
    #             dbmain.DB_str_n_one.ticker == self.ticker).first()
    #     return False # Создать перед началом сессии таблицу со стратегией и остановить стратегию
    # if not self.utlstr.check_trading_only_at_session(stngs.Settings.Strategies.Strategy_num_one_settings.trading_only_at_session):
    #     return False


def update_cels(data):
    with Session(autoflush=False, bind=engine) as db:
        qs_num_one = db.query(DB_str_n_one).filter(DB_str_n_one.ticker == data["ticker"],
                                                   DB_str_n_one.date == data["date"]).first()

    if qs_num_one != None:
        qs_num_one.type_signal = data.get("type_signal", None)
        qs_num_one.level_in = data.get("level_in", None)
        qs_num_one.support1 = data.get("support1", None)
        qs_num_one.support2 = data.get("support2", None)
        qs_num_one.resistance1 = data.get("resistance1", None)
        qs_num_one.resistance2 = data.get("resistance2", None)

        db.add(qs_num_one)
        db.commit()

    else:

        tom = DB_str_n_one(**data)
        db.add(tom)  # добавляем в бд
        db.commit()  # сохраняем изменения

def base_show(base):
    with Session(autoflush=False, bind=engine) as db:
        result = db.query(base).all()
        return result

def base_clear_all(db_name):
    with Session(autoflush=False, bind=engine) as db:
        db.query(db_name).delete()
        db.commit()

