import sys
sys.path.append("C:/Users/stasr/PycharmProjects/trading-bot/venv/Lib/site-packages")

import scripts.settings as stngs
# import scripts.settings_test as stngs_test
# import venv.Lib.

# Парсер входящих параметров
# import argparse

import pytz
from datetime import datetime

# import lib.lib.base1 as db

# import logging
from decimal import Decimal
import time
from threading import Event
# import telebot
from datetime import datetime, timezone, timedelta
import bot_trading.lib.strategies.main_strategies as mainstrat
import bot_trading.lib.trading.trading_main as trades
import bot_trading.lib.utilities.main_utilities as utilities
import bot_trading.lib.tinkoff.tinkoff_main as tinkoffmain
import bot_trading.lib.scripts.scripts_main as scr_main
import bot_trading.lib.scripts.figi as figi

import bot_trading.lib.db.db_main as dbmain

from tinkoff.invest import (
    CandleInstrument,
    Client,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
    MoneyValue
)

from tinkoff.invest.utils import decimal_to_quotation


from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float

################################################################################################# ИМПОРТЫ

TOKEN = stngs.Settings.TinkoffApi.Token.stas_sandbox


# logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# os.system("pause")

def add_money_sandbox(client, account_id, money, currency="rub"):
    """Function to add money to sandbox account."""
    money = decimal_to_quotation(Decimal(money))
    return client.sandbox.sandbox_pay_in(
        account_id=account_id,
        amount=MoneyValue(units=money.units, nano=money.nano, currency=currency),
    )

figi_temp1 = stngs.Settings.TinkoffApi.TickerFigi.vkco_figi
figi_temp2 = stngs.Settings.TinkoffApi.TickerFigi.sber_figi

dict = {1:SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE, 5: SubscriptionInterval.SUBSCRIPTION_INTERVAL_FIVE_MINUTES}

def main():
    "Подписка на стрим минутных свечей и их вывод examples/stream_client.py"
    #


    tickers_for_trade = scr_main.get_trade_tickers()

    utilities.Utility.otladka_print(txt=f"В тинькоф переданы следующие тикеры {[x for x in tickers_for_trade]}", lvl=2, end="\n\n")

    def request_iterator():
        try:
            yield MarketDataRequest(
                subscribe_candles_request=SubscribeCandlesRequest(
                    waiting_close=True,
                    subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                    instruments=[
                        CandleInstrument(
                            figi=figi.convert_ticker_to_figi(x),
                            interval=dict[stngs.Settings.Strategies.StrategiesMain.candle_period],
                            #interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                        ) for x in tickers_for_trade
                    ],
                )
            )
            while True:
                time.sleep(1)
        except:
            utilities.Utility.otladka_print(
                txt=f"🔴🔴🔴🔴 Тинькоф косячит. Ставлю паузу на 5 секунд и снова пробую обратиться к Тинькову",
                lvl=1, ticker=ticker_name)
            for _ in range(3):
                try:
                    Event().wait(5)
                    yield MarketDataRequest(
                        subscribe_candles_request=SubscribeCandlesRequest(
                            waiting_close=True,
                            subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                            instruments=[
                                CandleInstrument(
                                    figi=figi.convert_ticker_to_figi(x),
                                    interval=dict[stngs.Settings.Strategies.StrategiesMain.candle_period],
                                    # interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                                ) for x in tickers_for_trade
                            ],
                        )
                    )
                    while True:
                        time.sleep(1)
                except:
                    utilities.Utility.otladka_print(
                        txt=f"🔴🔴🔴🔴 Тинькоф косячит. через 5 секунд снова попробовал обратиться к Тинькову, но он все равно не ответил. Прекращаю программу.",
                        lvl=1, ticker=ticker_name)



        # yield MarketDataRequest(
        #     subscribe_candles_request=SubscribeCandlesRequest(
        #         waiting_close=True,
        #         subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
        #         instruments=[
        #             CandleInstrument(
        #                 figi=figi.convert_ticker_to_figi(x),
        #                 interval=dict[stngs.Settings.Strategies.StrategiesMain.candle_period],
        #                 #interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
        #             ) for x in tickers_for_trade
        #         ],
        #     )
        # )
        # while True:
        #     time.sleep(1)


    # def request_iterator():
    #     yield MarketDataRequest(
    #         subscribe_candles_request=SubscribeCandlesRequest(
    #             waiting_close=True,
    #             subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
    #             instruments=[
    #                 CandleInstrument(
    #                     figi='BBG000B9XRY4',
    #                     interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
    #                 )
    #             ],
    #         )
    #     )
    #     while True:
    #         time.sleep(1)


    with Client(TOKEN) as client:

        # obj = tinkoffmain.Orders()
        utilities.Utility.otladka_print(txt="🟩🟩🟩🟩🟩🟩🟩🟩 WITH CLIENT НАЧАЛСЯ", lvl=1)
        tickers_for_trade_temp = []
        col_tickers = 1

        for x in range(10):
            try:
                for marketdata in client.market_data_stream.market_data_stream(request_iterator()):
                    utilities.Utility.otladka_print(txt="Пришел ответ от Тинькова", lvl=9)
                    sec = utilities.Utility.current_utc_time()

                    # TODO В первую минуту торгов не должны приходить сиггнаолы
                    if (int(sec.strftime("%S")) <= 25 or int(sec.strftime("%S")) >= 55) or stngs.Settings.Strategies.StrategiesMain.candle_period == 5:
                        utilities.Utility.otladka_print(txt=f"\n\n------- 🔽🔽 ЦИКЛ ЗАПУЩЕН", lvl=4, end="\n")
                        # print(f"МОГУ ЛИ ПРОВЕРЯТЬ НА ЭТУ ВЕЛИЧИНУ? = {marketdata.candle}")
                        if marketdata.candle:
                            try:  # TODO Ставить try перед релизной версией
                                ticker_name = client.instruments.get_instrument_by(id_type=1, id=marketdata.candle.figi).instrument.ticker
                                rus_name = client.instruments.get_instrument_by(id_type=1, id=marketdata.candle.figi).instrument.name

                                # Создание и перебор списка тикеров
                                if stngs.Settings.Strategies.StrategiesMain.candle_period == 1:

                                    # Определение минуты
                                    sec_temp = sec + timedelta(seconds=6)
                                    # print("Минута", sec_temp.strftime("%M"))


                                    if len(tickers_for_trade_temp) == 0:
                                        tickers_for_trade_temp = tickers_for_trade.copy()
                                    if ticker_name not in tickers_for_trade_temp:
                                        continue
                                    if ticker_name in tickers_for_trade_temp:
                                        tickers_for_trade_temp.remove(ticker_name)
                                else:
                                    sec_temp = sec + timedelta(seconds=6)


                                if marketdata.candle.close.units:
                                    utilities.Utility.otladka_print(
                                        txt=f"------- {col_tickers} данные о котировке {rus_name} ({ticker_name}) получены = {utilities.Utility.convert_nano(marketdata.candle.close.units, marketdata.candle.close.nano)}",
                                        lvl=3, ticker=ticker_name)
                                    col_tickers += 1
                                else:
                                    utilities.Utility.otladka_print(txt=f"------- данные о котировке НЕ получены = - 🔴", lvl=1)
                                    continue
                                utilities.Utility.otladka_print(txt=f"------- В цикле Тинькова запущен figi = {marketdata.candle.figi}", lvl=4)

                                obj_strategy_num_three = mainstrat.Strategy()
                                obj_strategy_num_three.Strategy_num_three().main(ticker=ticker_name, candle_close=utilities.Utility.convert_nano(marketdata.candle.close.units, marketdata.candle.close.nano), candle_high=utilities.Utility.convert_nano(marketdata.candle.high.units, marketdata.candle.high.nano), candle_low=utilities.Utility.convert_nano(marketdata.candle.low.units, marketdata.candle.low.nano), rus_name=rus_name, minute=int(sec_temp.strftime("%M")), version=1)
                                # obj_strategy_num_three.Strategy_num_three().main(ticker=ticker_name, candle_close=utilities.Utility.convert_nano(marketdata.candle.close.units, marketdata.candle.close.nano), candle_high=utilities.Utility.convert_nano(marketdata.candle.high.units, marketdata.candle.high.nano), candle_low=utilities.Utility.convert_nano(marketdata.candle.low.units, marketdata.candle.low.nano), rus_name=rus_name, minute=int(sec_temp.strftime("%M")), version=2)

                                obj_strategy_simulate_trading = trades.TradingSimulate()
                                obj_strategy_simulate_trading.main(ticker=ticker_name, candle_close=utilities.Utility.convert_nano(marketdata.candle.close.units, marketdata.candle.close.nano), candle_high=utilities.Utility.convert_nano(marketdata.candle.high.units, marketdata.candle.high.nano), candle_low=utilities.Utility.convert_nano(marketdata.candle.low.units, marketdata.candle.low.nano), rus_name=rus_name, minute=int(sec_temp.strftime("%M")), version=1)
                                # obj_strategy_simulate_trading.main(ticker=ticker_name, candle_close=utilities.Utility.convert_nano(marketdata.candle.close.units, marketdata.candle.close.nano), candle_high=utilities.Utility.convert_nano(marketdata.candle.high.units, marketdata.candle.high.nano), candle_low=utilities.Utility.convert_nano(marketdata.candle.low.units, marketdata.candle.low.nano), rus_name=rus_name, minute=int(sec_temp.strftime("%M")), version=2)



                                if len(tickers_for_trade_temp) == 0 and stngs.Settings.Strategies.StrategiesMain.candle_period == 1:
                                    utilities.Utility.otladka_print(txt=f"Пришли данные по {col_tickers-1} тикерам", type_msg=2, lvl=4, ticker=ticker_name)
                                    col_tickers = 1
                                    Event().wait(55 - int(sec_temp.strftime("%S")))
                            except:
                                utilities.Utility.otladka_print(txt=f"🔴🔴🔴 Ошибка на стороне Тинькова", lvl=0)
                                msg = f"<b>Ошибка на стороне брокера. Перезапустите бота</b>"
                        else:
                            utilities.Utility.otladka_print(txt="Данные с сервера Тинькоф еще не пришли", type_msg=2, lvl=3)



                        utilities.Utility.otladka_print(txt="\n------- 🔼🔼 ЦИКЛ ЗАКОНЧИЛСЯ", lvl=4)
            except:
                utilities.Utility.otladka_print(txt="🟥🟥🟥 Ошибка итератора", lvl=0)
                Event().wait(2)
        utilities.Utility.otladka_print(txt="🟥🟥🟥🟥🟥🟥🟥 WITH CLIENT ЗАКОНЧИЛСЯ", lvl=1)

if __name__ == "__main__" and stngs.Settings.Strategies.StrategiesMain.tinkoff_start:
    main()
else:
    obj = tinkoffmain.Orders()


    ticker2 = "PLZL"
    # high2 = 9584.5
    # close2 = 9570.0
    # low2 = 9560.0
    # high2 = 9582.5
    # close2 = 9565.5
    # low2 = 9555.5
    high2 = 9803.0
    close2 = 9802.0
    low2 = 9801.0
    rus_name2 = "SBER"
    minute2 = 5


    obj_strategy_num_three = mainstrat.Strategy()
    obj_strategy_num_three.Strategy_num_three().main(ticker=ticker2, candle_high=high2, candle_close=close2, candle_low=low2,
                                                 rus_name=rus_name2, minute=minute2, version=1)
    # obj_strategy_num_three.Strategy_num_three().main(ticker=ticker2, candle_high=high2, candle_close=close2, candle_low=low2,
    #                                              rus_name=rus_name2, minute=minute2, version=2)


    # obj_strategy_simulate_trading = trades.TradingSimulate()
    # obj_strategy_simulate_trading.main(ticker=ticker2, candle_high=high2, candle_close=close2, candle_low=low2,
    #                                              rus_name=rus_name2, minute=minute2, version=1)
    # obj_strategy_simulate_trading.main(ticker=ticker2, candle_high=high2, candle_close=close2, candle_low=low2,
    #                                              rus_name=rus_name2, minute=minute2, version=2)
