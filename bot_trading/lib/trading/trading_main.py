import bot_trading.lib.utilities.main_utilities as utl
import bot_trading.lib.tinkoff.tinkoff_main as tinkoffmain
import bot_trading.lib.db.db_main as dbmain
import bot_trading.lib.db.db_scripts as dbscripts

from sqlalchemy.orm import Session
from bot_trading.lib.db.db_main import DB_str_trading_simulate, engine

class TradingSimulate:
    def main(self, ticker, candle_close=0, rus_name="", start_time="", candle_high=0, candle_low=0, minute=None, start=0, strategy_name="", version=1):

        # with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
        #     qs_tickers_for_trading = db.query(dbmain.DB_str_n_three).filter(
        #         dbmain.DB_str_n_three.candle_x2_name != None,
        #         dbmain.DB_str_n_three.date == utl.Utility.current_date(),
        #         dbmain.DB_str_n_three.ticker == ticker).first()
        #
        # with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
        #     qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
        #         dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
        #         dbmain.DB_str_trading_simulate.ticker == ticker,
        #         dbmain.DB_str_trading_simulate.stop_loss_value == None
        #
        #     ).first()

        utl.Utility.otladka_print(
            txt=f"{rus_name} ({ticker}) Зашел на проверку симуляции торговли",
            lvl=4,
            ticker=ticker)

        if start == 1:

            utl.Utility.otladka_print(
                txt=f"{rus_name} ({ticker}) Получен сигнал на торговлю для выставления лимитной заявки",
                lvl=3,
                ticker=ticker)

            # Проверка на сигнал, который запустил стратегию
            with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
                qs_str_n_three = db.query(dbmain.DB_str_n_three).filter(
                    dbmain.DB_str_n_three.candle_x2_name != None,
                    dbmain.DB_str_n_three.date == utl.Utility.current_date(),
                    dbmain.DB_str_n_three.ticker == ticker,
                    dbmain.DB_str_n_three.version == version,
                ).first()


            # Проверка на то, есть ли уже запущенная стратегия, но не было входа. Если есть, то удаляю предыдущую не запущенную сделку
            with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
                qs_ticker_for_trading_2 = db.query(dbmain.DB_str_trading_simulate).filter(
                    dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
                    dbmain.DB_str_trading_simulate.ticker == ticker,
                    dbmain.DB_str_trading_simulate.version == version,
                    dbmain.DB_str_trading_simulate.trade_out_value == None,
                    dbmain.DB_str_trading_simulate.trade_in_value == None
                ).first()
            if qs_ticker_for_trading_2:
                utl.Utility.otladka_print(
                    txt=f"{rus_name} ({ticker}) Есть уже запущенная стратегия, но не было входа. Удаляю предыдущую не запущенную сделку",
                    lvl=3,
                    ticker=ticker)
                db.delete(qs_ticker_for_trading_2)
                db.commit()

            # Проверка на работающуюу стратегию
            with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
                qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
                    dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
                    dbmain.DB_str_trading_simulate.ticker == ticker,
                    dbmain.DB_str_trading_simulate.version == version,
                    dbmain.DB_str_trading_simulate.trade_out_value == None,
                    dbmain.DB_str_trading_simulate.trade_in_value != None
                ).first()

            # Если пришел сигнал на тот же уровень, но бот все еще находится в сделке по предыдущему сигналу
            if qs_ticker_for_trading and qs_str_n_three.candle_x2_name and qs_ticker_for_trading.strategy_level_name \
                    and qs_str_n_three.candle_x2_name == qs_ticker_for_trading.strategy_level_name \
                    and qs_ticker_for_trading.trade_in_value != None \
                    and qs_ticker_for_trading.trade_out_value == None:
                utl.Utility.otladka_print(
                    txt=f"{rus_name} ({ticker}) Сигнал пришел сигнал на тот же уровень, но бот все еще находится в сделке по предыдущему сигналу.",
                    lvl=3,
                    ticker=ticker)
                return False

            # Если пришел сигнал на другой уровень, но бот все еще находится в сделке по предыдущему сигналу. То есть по более выгодному
            # print(f"{qs_str_n_three.candle_x2_name}")
            # print(qs_str_n_three.candle_x2_name != qs_ticker_for_trading.strategy_level_name)
            # print(qs_ticker_for_trading.trade_in_value)
            # print(qs_ticker_for_trading.trade_out_value)

            if qs_str_n_three.candle_x2_name and qs_ticker_for_trading \
                    and qs_str_n_three.candle_x2_name != qs_ticker_for_trading.strategy_level_name \
                    and qs_ticker_for_trading.trade_in_value \
                    and not qs_ticker_for_trading.trade_out_value \
                    :
                utl.Utility.otladka_print(
                    txt=f"{rus_name} ({ticker}) Сигнал пришел на другой уровень, но бот все еще находится в сделке по предыдущему сигналу. То есть по более выгодному. Так что оставляю старую сделку.",
                    lvl=3,
                    ticker=ticker)
                return False

            # Зайти еще раз в сделку если по этому же уровню уже, так как ранее получил стоп лосс
            if qs_str_n_three.candle_x2_name and qs_ticker_for_trading\
                    and qs_str_n_three.candle_x2_name == qs_ticker_for_trading.strategy_level_name \
                    and qs_ticker_for_trading.trade_in_value \
                    and qs_ticker_for_trading.trade_out_value \
                    :
                utl.Utility.otladka_print(
                    txt=f"{rus_name} ({ticker}) Зашел еще раз в сделку если по этому же уровню уже, так как ранее получил стоп лосс.",
                    lvl=3,
                    ticker=ticker)
                pass

            if (
                    qs_str_n_three.candle_x2_name and qs_ticker_for_trading \
                    and qs_str_n_three.candle_x2_name == qs_ticker_for_trading.strategy_level_name \
                    and qs_ticker_for_trading.trade_in_value \
                    and qs_ticker_for_trading.trade_out_value \
                    ) \
                    or not qs_ticker_for_trading:

                # if qs_ticker_for_trading:
                level_dict = {"level_in": "Базовый уровень", "resistance1": "Сопротивление 1",
                              "resistance2": "Сопротивление 2", "support1": "Поддержка 1", "support2": "Поддержка 2"}
                utl.Utility.otladka_print(
                    txt=f"{rus_name} ({ticker}) Добавление тикера для симуляции торговли от уровня \"{level_dict[qs_str_n_three.candle_x2_name]}\"",
                    lvl=2,
                    ticker=ticker)
                data = {}

                data["date"] = utl.Utility.current_date()
                data["ticker"] = ticker
                data["create_time"] = utl.Utility.current_utc_time()
                data["type_signal"] = qs_str_n_three.type_signal
                data["strategy_name"] = strategy_name
                data["version"] = version
                data["strategy_level_value"] = qs_str_n_three.candle_x2_value
                data["strategy_level_name"] = qs_str_n_three.candle_x2_name
                data["time_signal"] = qs_str_n_three.candle_x2_time
                data["last_price"] = candle_close
                data["update_time"] = utl.Utility.current_utc_time()
                data["update_minute"] = int(utl.Utility.current_utc_time().strftime("%M"))

                if qs_str_n_three.type_signal == "Лонг":
                    data["limit_value"] = float('{:.2f}'.format(qs_str_n_three.candle_x2_value * 1.001))
                    data["stop_loss_value"] = float('{:.2f}'.format(data["limit_value"] * 0.997))
                elif qs_str_n_three.type_signal == "Шорт":
                    data["limit_value"] = float('{:.2f}'.format(qs_str_n_three.candle_x2_value * 0.999))
                    data["stop_loss_value"] = float('{:.2f}'.format(data["limit_value"] * 1.003))

                with Session(autoflush=False, bind=engine) as db:
                    tom = DB_str_trading_simulate(**data)
                    db.add(tom)  # добавляем в бд
                    db.commit()  # сохраняем изменения

                with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
                    qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
                        dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
                        dbmain.DB_str_trading_simulate.ticker == ticker,
                        dbmain.DB_str_trading_simulate.version == version
                    ).first()

        with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
            qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
                dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
                dbmain.DB_str_trading_simulate.ticker == ticker,
                dbmain.DB_str_trading_simulate.trade_out_value == None,
                dbmain.DB_str_trading_simulate.version == version
            ).first()

        # Если по тикеру нет никаких сделок
        if not qs_ticker_for_trading:
            return False

        # Если инструмент уже вышел из сделки
        # if qs_ticker_for_trading.trade_out_time:
        #     utl.Utility.otladka_print(
        #         txt=f"{rus_name} ({ticker}) Инструмент уже вышел из сделки",
        #         lvl=2,
        #         ticker=ticker)
        #     return False

        # Установка delta price
        if qs_ticker_for_trading.type_signal == "Лонг":
            delta_price = 100 * ((candle_close - qs_ticker_for_trading.limit_value) / candle_close)
        elif qs_ticker_for_trading.type_signal == "Шорт":
            delta_price = 100 * ((qs_ticker_for_trading.limit_value - candle_close) / qs_ticker_for_trading.limit_value)
        delta_price = float('{:.2f}'.format(delta_price))
        for _ in [['delta_price', delta_price],
                  ['last_price', candle_close],
                  ['update_time', utl.Utility.current_utc_time()],
                  ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))]
                  ]:
            dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])

        # Вход в сделку
        if not qs_ticker_for_trading.trade_in_value:
            if (candle_high >= qs_ticker_for_trading.limit_value and qs_ticker_for_trading.type_signal == "Лонг") or\
                (candle_low <= qs_ticker_for_trading.limit_value and qs_ticker_for_trading.type_signal == "Шорт")\
            :
                utl.Utility.otladka_print(
                    txt=f"{rus_name} ({ticker}) Вхожу в сделку на уровне {qs_ticker_for_trading.limit_value}",
                    lvl=2,
                    ticker=ticker)

                type_round = {"Лонг": "🟢", "Шорт": "🔴"}
                type_move_short = {"Лонг": "🔼", "Шорт": "🔽"}

                msg = f"<u>Вхожу в сделку в {qs_ticker_for_trading.type_signal} от уровня {qs_ticker_for_trading.limit_value}\n\n</u>"\
                      f"<b>{rus_name} ({ticker}) :: {qs_ticker_for_trading.type_signal} {type_round[qs_ticker_for_trading.type_signal]}</b>\n\n" \
                      f"<b>Текущая цена: {candle_close} {type_move_short[qs_ticker_for_trading.type_signal]}</b>" \


                # print(msg)
                #
                # if not utl.Utility.send_msg_to_group(msg):
                #     utl.Utility.otladka_print(
                #         txt=f"🔴🔴🔴🔴 Торговый бот не смог отправить сообщение в телеграм",
                #         lvl=0, ticker=ticker)


                for _ in [['trade_in_value', qs_ticker_for_trading.limit_value],
                          ['trade_in_time', utl.Utility.current_utc_time()]
                          ]:
                    dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
                with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
                    qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
                        dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
                        dbmain.DB_str_trading_simulate.ticker == ticker,
                        dbmain.DB_str_trading_simulate.version == version
                    ).first()

            # До сих пор не вошел в сделку
            else:
                return False

        # Стоп лосс
        if candle_low <= qs_ticker_for_trading.stop_loss_value and qs_ticker_for_trading.type_signal == "Лонг":
            utl.Utility.otladka_print(
                txt=f"{rus_name} ({ticker}) Стоп лосс {qs_ticker_for_trading.stop_loss_value} ({float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - qs_ticker_for_trading.stop_loss_value) / qs_ticker_for_trading.trade_in_value)))}%)",
                lvl=2,
                ticker=ticker)

            type_round = {"Лонг": "🟢", "Шорт": "🔴"}
            type_move_short = {"Лонг": "🔼", "Шорт": "🔽"}

            msg = f"🔴 Стоп-лосс составил {float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - qs_ticker_for_trading.stop_loss_value) / qs_ticker_for_trading.trade_in_value)))}%" \
                  f"<b>{rus_name} ({ticker}) :: {qs_ticker_for_trading.type_signal}</b>\n\n" \
                  f"<b>Текущая цена: {candle_close} {type_move_short[qs_ticker_for_trading.type_signal]}</b>\n\n" \
                  f"Стоп-лосс по сделке в {qs_ticker_for_trading.type_signal} от уровня {qs_ticker_for_trading.limit_value}\n"\


            # print(msg)
            #
            # if not utl.Utility.send_msg_to_group(msg):
            #     utl.Utility.otladka_print(
            #         txt=f"🔴🔴🔴🔴 Торговый бот не смог отправить сообщение в телеграм",
            #         lvl=0, ticker=ticker)

            for _ in [['trade_out_value', qs_ticker_for_trading.stop_loss_value],
                      ['trade_out_time', utl.Utility.current_date()],
                      ['percent_loss', float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - qs_ticker_for_trading.stop_loss_value) / qs_ticker_for_trading.trade_in_value)))]
                      ]:
                dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
            return False
        elif candle_high >= qs_ticker_for_trading.stop_loss_value and qs_ticker_for_trading.type_signal == "Шорт":
            utl.Utility.otladka_print(
                txt=f"{rus_name} ({ticker}) Стоп лосс {qs_ticker_for_trading.stop_loss_value} ({float('{:.2f}'.format(100 * ((qs_ticker_for_trading.stop_loss_value - qs_ticker_for_trading.trade_in_value) / qs_ticker_for_trading.stop_loss_value)))}%)",
                lvl=2,
                ticker=ticker)
            for _ in [['trade_out_value', qs_ticker_for_trading.stop_loss_value],
                      ['trade_out_time', utl.Utility.current_date()],
                      ['percent_loss', float('{:.2f}'.format(100 * ((qs_ticker_for_trading.stop_loss_value - qs_ticker_for_trading.trade_in_value) / qs_ticker_for_trading.stop_loss_value)))]
                      ]:
                dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
            return False

        # Сохранение максимально прибыльной цены
        data = {}
        if qs_ticker_for_trading.type_signal == "Лонг" and (
                (qs_ticker_for_trading.max_price and qs_ticker_for_trading.max_price < candle_high) or
                not qs_ticker_for_trading.max_price
        ):
            utl.Utility.otladka_print(
                txt=f"{rus_name} ({ticker}) Зафиксировал максимальную прибыль {candle_high} ({float('{:.2f}'.format(100 * ((candle_high - qs_ticker_for_trading.trade_in_value) / candle_high)))}%)",
                lvl=2,
                ticker=ticker)
            for _ in [['max_price', candle_high],
                      ['percent_win', float('{:.2f}'.format(100 * ((candle_high - qs_ticker_for_trading.trade_in_value) / candle_high)))]
                      ]:
                dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
        elif qs_ticker_for_trading.type_signal == "Шорт" and (
                (qs_ticker_for_trading.max_price and candle_low < qs_ticker_for_trading.max_price) or
                not qs_ticker_for_trading.max_price
        ):
            utl.Utility.otladka_print(
                txt=f"{rus_name} ({ticker}) Зафиксировал максимальную прибыль {candle_low} ({float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - candle_low) / qs_ticker_for_trading.trade_in_value)))}%)",
                lvl=2,
                ticker=ticker)
            for _ in [['max_price', candle_low],
                      ['percent_win', float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - candle_low) / qs_ticker_for_trading.trade_in_value)))]
                      ]:
                dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])

        # Изменения стопа лосса в б/у, если цена ушла дальше +0,6%
        if qs_ticker_for_trading.percent_win and qs_ticker_for_trading.percent_win >= 0.6 and qs_ticker_for_trading.stop_loss_value != qs_ticker_for_trading.limit_value:
            utl.Utility.otladka_print(
                txt=f"{rus_name} ({ticker}) Изменения стопа в б/у, так как цена ушла дальше +0,6%",
                lvl=2,
                ticker=ticker)
            for _ in [['stop_loss_value',  qs_ticker_for_trading.limit_value]
                      ]:
                dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
            return False
