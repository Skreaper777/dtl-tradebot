import scripts.settings as stngs
import bot_trading.lib.utilities.main_utilities as utl
import bot_trading.lib.tinkoff.tinkoff_main as tinkoffmain
import bot_trading.lib.db.db_main as dbmain
import bot_trading.lib.db.db_scripts as dbscripts
from datetime import datetime

class Strategy:
    @staticmethod
    def strategy_flat_simple(obj, type_str, signal_in, current_value):
        """
        Стратегия Боковик

        :param obj:
        :param type_str:
        :param signal_in:
        :param current_value:
        :return:
        """

        if type_str == 'long' and \
                current_value > signal_in and \
                not obj.get_open_orders():

            if obj.open_ticket_buy():

                obj.set_open_orders(True)
                msg = f"Успешно открыл сделку. Купил и установил параметр в Orders open_orders = {obj.open_orders}"
                # Files("txt\\test1.txt", "+a").write_file(msg)

                #### Отладка ####
                if stngs.Settings.Development.otladka:
                    utl.Utility.otladka_print(type_msg=2, txt=msg, end="\n\n")
                    pass
            else:
                utl.Utility.otladka_print(type_msg=2, txt=f"Не стал покупать, так как произошла ошибка во время сделки",
                                      end="\n\n")

        elif type_str == 'short' and \
                current_value < signal_in and \
                not obj.get_open_orders():

            if obj.open_ticket_sell():
                obj.set_open_orders(True)
                msg = f"Успешно открыл сделку. Продал и установил параметр в Orders open_orders = {obj.open_orders}"
                # Files("txt\\test1.txt", "+a").write_file(msg)
                utl.Utility.otladka_print(type_msg=2, txt=msg, end="\n\n") if stngs.Settings.Development.otladka else None
            else:
                utl.Utility.otladka_print(type_msg=2, txt=f"Не стал продавать, так как произошла ошибка во время сделки",
                                      end="\n\n")

        elif obj.get_open_orders():
            utl.Utility.otladka_print(type_msg=2, txt=f"Не вхожу в сделку, так как уже есть одна открытая",
                                  end="\n\n")

    class
    @staticmethod
    def strategy_num_one(ticker, candle_close=0, rus_name="", start_time=""):
        lenght_candle = 0.001
        price_ticker = 1
        utl.Utility.otladka_print(txt="Запустилась стратегия номер 1", lvl=2)
        pass_reason = 0
        start_at_session = stngs.Settings.Strategies.Strategy_num_one_settings.trading_only_at_session == 1



        # выборка текущего тикера из таблицы стратегии
        with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
            qs_num_one = db.query(dbmain.DB_str_n_one).filter(dbmain.DB_str_n_one.ticker == ticker).first()

        # Если в таблице стратегии еще не создана строка с тикером, то создать ее
        if not qs_num_one:
            with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
                # print(db.query(dbmain.Signals).filter(dbmain.Signals.ticker == ticker).first().__dict__)
                query_signals = db.query(dbmain.Signals).filter(dbmain.Signals.ticker == ticker).first()

            level_in = query_signals.level_in
            with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
                query = dbmain.DB_str_n_one(ticker=ticker, level_in=level_in, type_signal=query_signals.type_signal, last_update=utl.Utility.current_utc_time())
                db.add(query)
                db.commit()
            # выборка текущего тикера из таблицы стратегии
            with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
                qs_num_one = db.query(dbmain.DB_str_n_one).filter(
                    dbmain.DB_str_n_one.ticker == ticker).first()

        # Проверка на начало торговой сессии
        if start_at_session and int(utl.Utility.current_utc_time().strftime("%H")) < 7:
            return False

        timedif = utl.Utility.current_utc_time() - datetime.strptime(qs_num_one.last_update, "%Y-%m-%d %H:%M:%S.%f%z")
        utl.Utility.otladka_print(txt=f"Разница во времени между запросами стратегии составлет {timedif.total_seconds()} секунд", lvl=2)

        # cur_hour =
        # cur_min =

        if not qs_num_one.pass_reason and timedif.total_seconds() > 55:
            level_in = qs_num_one.level_in

            # Присвоение каждой новой свече значение параметра close
            with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
                qs_candle_close = db.query(dbmain.DB_str_n_one).filter(dbmain.DB_str_n_one.ticker == ticker).first()
                play = 1
                candle = 1
                while play:
                    if qs_candle_close.__dict__['candle_close_'+str(candle)]:
                        candle += 1
                    else:
                        setattr(qs_candle_close, 'candle_close_'+str(candle), candle_close)
                        db.commit()
                        play = 0
            ############# 1 свеча
            if candle == 1:
                utl.Utility.otladka_print(txt=f"{rus_name} ({ticker}) проходит проверку на 1ую свечу", lvl=2)
                dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'last_update',
                                         utl.Utility.current_utc_time())
                if candle_close > level_in:
                    pass
                else:
                    pass_reason = "Первая свеча закрылась ниже уровня входа"
                    dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'pass_reason', pass_reason)
                    pass

            ############# 2 свеча
            elif candle == 2:
                utl.Utility.otladka_print(txt=f"{rus_name} ({ticker}) проходит проверку на 2ую свечу", lvl=2)
                dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'last_update',
                                         utl.Utility.current_utc_time())
                if candle_close < level_in:
                    pass
                else:
                    pass_reason = "Вторая свеча закрылась выше уровня входа"
                    dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'pass_reason', pass_reason)
                    pass
            ############# 3 свеча
            elif candle == 3:
                utl.Utility.otladka_print(txt=f"{rus_name} ({ticker}) проходит проверку на 3ью свечу", lvl=2)
                dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'last_update',
                                         utl.Utility.current_utc_time())
                delta_atr = 0.008
                if candle_close < level_in and lenght_candle / price_ticker <= delta_atr:
                    msg = f"<b>{rus_name} ({ticker})</b>\n" \
                          f"{qs_num_one.type_signal} 🟢\n\n" \
                          f"Текущая цена: {candle_close}    (уровень входа: {level_in})\n" \
                          f"Цена готовится пробить уровень входа {level_in} снизу-вверх 🔼. \n" \
                          f"Подготовтесь к сделке. \n\n" \
                          f"<i>(Свеча 3)</i>"

                    print(msg)
                    utl.Utility.send_msg_to_group(msg)
                else:
                    if candle_close >= level_in:
                        pass_reason = "Третья свеча закрылась выше уровня входа"
                        dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'pass_reason', pass_reason)
                    elif lenght_candle / price_ticker > delta_atr:
                        pass_reason = f"АТР третьей свечи больше {delta_atr*100}%"
                        dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'pass_reason', pass_reason)
            ############# 4 свеча
            elif candle == 4:
                utl.Utility.otladka_print(txt=f"{rus_name} ({ticker}) проходит проверку на 4ую свечу", lvl=2)
                delta_atr = 0.006
                dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'last_update',
                                         utl.Utility.current_utc_time())
                if candle_close < level_in and lenght_candle / price_ticker <= delta_atr:
                    msg = f"<b>{rus_name} ({ticker})</b>\n" \
                          f"{qs_num_one.type_signal} 🟢\n\n" \
                          f"Текущая цена: {candle_close}    (уровень входа: {level_in})\n" \
                          f"Цена готовится пробить уровень входа {level_in} снизу-вверх 🔼. \n" \
                          f"Подготовтесь к сделке. \n\n" \
                          f"<i>(Свеча 4)</i>"
                    print(msg)
                    utl.Utility.send_msg_to_group(msg)
                else:
                    if candle_close >= level_in:
                        pass_reason = "Четвертая свеча закрылась выше уровня входа"
                        dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'pass_reason', pass_reason)
                    elif lenght_candle / price_ticker > delta_atr:
                        pass_reason = f"АТР четвертой свечи больше {delta_atr*100}%"
                        dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'pass_reason', pass_reason)
            ############# 5 свеча
            elif candle == 5:
                utl.Utility.otladka_print(txt=f"{rus_name} ({ticker}) проходит проверку на 5ую свечу", lvl=2)
                dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'last_update',
                                         utl.Utility.current_utc_time())
                if candle_close >= level_in:
                    msg = f"{rus_name} ({ticker}): Свеча 5 пробила уровень. Вход в сделку - успешный."
                    print(msg)
                    utl.Utility.send_msg_to_group(msg)
                else:
                    pass_reason = "Пятая свеча закрылась ниже уровня входа"
                    dbscripts.db_update_cell(dbmain.DB_str_n_one, ticker, 'pass_reason', pass_reason)
        else:
            utl.Utility.otladka_print(txt=f"Не стал заходить в стратегию, так как прошло слишком мало времени или бумага уже вышла из параметров стратегии", lvl=2)

        return True

