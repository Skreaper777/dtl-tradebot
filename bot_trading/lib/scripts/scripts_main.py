# import scripts.settings as stngs
# import bot_trading.lib.utilities.main_utilities as utilities
import bot_trading.lib.tinkoff.tinkoff_main as tinkoffmain
import bot_trading.lib.db.db_main as dbmain
import bot_trading.lib.utilities.main_utilities as utl

# import bot_trading.lib.db.db_scripts as dbscripts

def get_trade_tickers():
    """
    Возвращает список тикеров из таблицы сигналы
    :return:
    """
    with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
        q_signals_all = db.query(dbmain.Signals).filter(dbmain.Signals.date == utl.Utility.current_date()).all()

        # q_signals_all = db.query(dbmain.Signals).all()

        return [db_ticker.ticker for db_ticker in q_signals_all]

# def checking_ticker_ready_to_trade(db_ticker):
#     if db_ticker.type_signal:
#         return True
#     else:
#         return False