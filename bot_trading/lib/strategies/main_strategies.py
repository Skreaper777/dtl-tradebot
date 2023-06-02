import scripts.settings as stngs
import bot_trading.lib.utilities.main_utilities as utl
import bot_trading.lib.tinkoff.tinkoff_main as tinkoffmain
import bot_trading.lib.db.db_main as dbmain
import bot_trading.lib.db.db_scripts as dbscripts
from datetime import datetime
import bot_trading.lib.trading.trading_main as trades
from sqlalchemy.orm import Session
from bot_trading.lib.db.db_main import DB_str_trading_simulate, engine


class Strategy:
    class Functions:
        def start_check(self):
            # time_now = utl.Utility.current_utc_time()
            # time_now = time.strftime("%H:%M:%S", time_now)
            # print(utl.Utility.current_utc_time())
            # print(utl.Utility.current_date())

            # выборка текущего тикера из таблицы стратегии

            # with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
            #     # self.qs_num_one = db.query(dbmain.DB_str_n_one).filter(dbmain.DB_str_n_one.ticker == self.ticker, dbmain.DB_str_n_one.date == utl.Utility.current_date()).first()
            #     # print(dbmain.DB_str_n_two.__dict__)
            #     # self.qs_num_two = db.query(dbmain.DB_str_n_two).filter(dbmain.DB_str_n_two.ticker == self.ticker,
            #     #                                                        dbmain.DB_str_n_two.date == utl.Utility.current_date()).first()
            #     self.qs_num_three = db.query(dbmain.DB_str_n_three).filter(dbmain.DB_str_n_three.ticker == self.ticker,
            #                                                            dbmain.DB_str_n_three.date == utl.Utility.current_date()).first()
            # Если в таблице стратегии еще не создана строка с тикером, то создать ее
            # if not self.qs_num_one:
            #     # with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
            #     #     # print(db.query(dbmain.Signals).filter(dbmain.Signals.ticker == ticker).first().__dict__)
            #     #     query_signals = db.query(dbmain.Signals).filter(dbmain.Signals.ticker == self.ticker).first()
            #     #
            #     # level_in = query_signals.level_in
            #     # with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
            #     #     query = dbmain.DB_str_n_one(ticker=self.ticker, level_in=level_in, type_signal=query_signals.type_signal, last_update=utl.Utility.current_utc_time())
            #     #     db.add(query)
            #     #     db.commit()
            #     # # выборка текущего тикера из таблицы стратегии
            #     # with tinkoffmain.Session(autoflush=False, bind=tinkoffmain.engine) as db:
            #     #     self.qs_num_one = db.query(dbmain.DB_str_n_one).filter(
            #     #         dbmain.DB_str_n_one.ticker == self.ticker).first()
            #     # return False # Создать перед началом сессии таблицу со стратегией и остановить стратегию
            #     utl.Utility.otladka_print(txt="Сигналы на сегодняшнюю дату еще не были загружены", lvl=0)
            #     return False
            if not self.qs_num_three:
                utl.Utility.otladka_print(txt="🔴 Сигналы на сегодняшнюю дату еще не были загружены", lvl=0, ticker=self.ticker)
                return False
            if not utl.UtilityStratagies.check_trading_only_at_session(stngs.Settings.Strategies.Strategy_num_three_settings.trading_only_at_session) :
                return False
            if not utl.UtilityStratagies.check_trading_period(stngs.Settings.Strategies.Strategy_num_three_settings.trading_period) :
                return False

            # if self.qs_num_one.last_update != None:
            #     self.timedif = utl.Utility.current_utc_time() - datetime.strptime(self.qs_num_one.last_update, "%Y-%m-%d %H:%M:%S.%f%z")
            #     self.timedif = self.timedif.seconds
            #     utl.Utility.otladka_print(txt=f"Разница во времени между запросами стратегии составлет {self.timedif} секунд", lvl=2)
            # else:
            #     self.timedif=999
            #     utl.Utility.otladka_print(
            #         txt=f"Зашел в проверку и установил timedif=999", lvl=2)

            # if self.timedif < stngs.Settings.Strategies.Strategy_num_one_settings.dif_between_query:
            #     utl.Utility.otladka_print(
            #         txt=f"Не стал заходить в стратегию, так как прошло слишком мало времени между обновлениями данных",
            #         lvl=2)
            #     return False

            if self.qs_num_three.pass_reason:
                utl.Utility.otladka_print(txt=f"{self.rus_name} ({self.ticker}) Бумага уже вышла из своей стратегии", lvl=3, ticker=self.ticker)
                return False



            # if not self.utlstr.check_candle_by_minute(ccat, 7, 10, self.num_candle):
            #     return False

            utl.Utility.otladka_print(txt="Все стартовые проверки прошли успешно", lvl=4, ticker=self.ticker)
            return True
        def strategy_num_three_delete_candles(self):
            if self.qs_num_three.level_name:
                for x in range(3):
                    for _ in [['candle_x' + str(x) + '_name', None],
                              ['candle_x' + str(x) + '_last_price', None],
                              ['candle_x' + str(x) + '_value', None],
                              ['candle_x' + str(x) + '_time', None],
                              ['candle_x' + str(x) + '_minute', None],
                              ['update_time', utl.Utility.current_utc_time()],
                              ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                              ]:
                        dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])

        def strategy_num_three_delete_level(self):
            if self.qs_num_three.level_name:

                for _ in [["level_name", None],
                          ["level_value", None],
                          ['update_time', utl.Utility.current_utc_time()],
                          ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                          ]:
                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])

        def set_day_highlow(self):
            if (self.qs_num_three.day_high and self.qs_num_three.day_high < self.candle_high) or not self.qs_num_three.day_high:
                for _ in [["day_high", self.candle_high]
                          ]:
                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                self.day_high = self.candle_high
            if (self.qs_num_three.day_low and self.qs_num_three.day_low > self.candle_low) or not self.qs_num_three.day_low:
                for _ in [["day_low", self.candle_low]
                          ]:
                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                self.day_low = self.candle_low

    class Strategy_num_three:
        def main(self, ticker, candle_close=0, rus_name="", start_time="", candle_high=0, candle_low=0, minute=None, version=1):
            # ticker = ticker
            # candle_high = high
            # candle_low = low
            # candle_close = candle_close
            # rus_name = rus_name

            self.ticker = ticker
            self.rus_name = rus_name
            self.candle_high = candle_high
            self.candle_low = candle_low

            versions = {1: "Проторговка :: базовая версия", 2: "Проторговка 2 :: Не более 1,2% от базового уровня в сторону сделки"}
            versions_tlgm = {1: "№1", 2: "№2"}
            strategy_name = versions[version]

            utl.Utility.otladka_print(txt=f"Запустилась стратегия \"{strategy_name}\"", lvl=3, ticker=ticker)
            utlstr = utl.UtilityStratagies

            with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
                self.qs_num_three = db.query(dbmain.DB_str_n_three).filter(
                    dbmain.DB_str_n_three.ticker == ticker,
                    dbmain.DB_str_n_three.date == utl.Utility.current_date(),
                    dbmain.DB_str_n_three.version == version,
                ).first()



            # Стартовые проверки
            if not Strategy.Functions.start_check(self):
                return False

            level_in = self.qs_num_three.level_in
            atr_out = stngs.Settings.Strategies.Strategy_num_three_settings.sbros_stratefii_atr_out
            atr_high = stngs.Settings.Strategies.Strategy_num_three_settings.sbros_stratefii_atr_high
            atr_low = stngs.Settings.Strategies.Strategy_num_three_settings.sbros_stratefii_atr_low
            cshet_kasaniy = stngs.Settings.Strategies.Strategy_num_three_settings.cshet_kasaniy

            ts = self.qs_num_three.type_signal
            max_level = self.qs_num_three.max_level
            min_level = self.qs_num_three.min_level
            ld = {}
            # level_dict = {"Базовый уровень" : "level_in", "Сопротивление 1" : "resistance1", "Сопротивление 2" : "resistance2", "Поддержка 1" : "support1", "Поддержка 2" : "support2"}
            level_dict = {"level_in": "Базовый уровень", "resistance1": "Сопротивление 1",
                          "resistance2": "Сопротивление 2", "support1": "Поддержка 1", "support2": "Поддержка 2"}

            koridor = 0
            napr = {"Лонг": -1, "Шорт": 1}
            step = self.qs_num_three.step

            level_names_dict = {-2: "support2", -1: "support1", 0: "level_in", 1: "resistance1",
                                2: "resistance2"}

            # if step:
            #     ld = {"Лонг": [-2, -1, 0, 1], "Шорт": [-1, 0, 1, 2]}
            #     # TODO Сделать удаление уровней, если цена ушла к дальним уровням
            # # elif not step
            # else:
            #     ld = {"Лонг": [], "Шорт": []}
            #     for key, value in level_names_dict:
            #         if value:
            #             # self.qs_num_three.__dict__[values]
            #             ld = {self.qs_num_three.__dict__[key]: self.qs_num_three.__dict__[value]}
            #
            #             # ld = {"Лонг": [0], "Шорт": [0]}
            #     step = 0





            if step:
                if ts == "Лонг":
                    for x in range(-2,2):
                        ld[level_names_dict[x]] = level_in + step * x
                elif ts == "Шорт":
                    for x in range(-1,3):
                        ld[level_names_dict[x]] = level_in + step * x
            else:
                step = 0
                levels = []
                for key, level_name_d in level_names_dict.items():
                    if self.qs_num_three.__dict__[level_name_d]:
                        # self.qs_num_three.__dict__[values]
                        ld[level_name_d] = self.qs_num_three.__dict__[level_name_d]
                        levels.append(self.qs_num_three.__dict__[level_name_d])

            current_level_number= -1

            # Перебор уровней в цикле
            for level_eng_name_c, level_value_c in ld.items():
                current_level_number+= 1
                level_name = level_eng_name_c

                utl.Utility.otladka_print(txt=f"{self.rus_name} ({self.ticker}) рассматриваемый уровень {level_name}",
                                          lvl=8, ticker=self.ticker)

                if not self.qs_num_three.candle_x1_name:
                    atr_in = atr_high
                else:
                    atr_in = atr_low

                # это значение текущего рассматриваемого уровня
                current_level_value = level_value_c
                # Это атр первого или второго бара для проторговки
                base_border = current_level_value * (1 + atr_in / 100 * napr[ts])
                # в одном из случаев этот параметр был равен 1% в виде значения цены а не процентов
                base_out = current_level_value * (1 + atr_out / 100 * napr[ts])

                if step:
                    # здесь просто определяется верхний и нижнмий уровни (их значения), если имеется параметр шага уровней step
                    upper_level = current_level_value + step
                    bottom_level = current_level_value - step

                    # определение последнего минимально возможного уровня от которого можно войти в сделку
                    if ts == "Лонг":
                        if current_level_number == len(ld):
                            # upper_level = current_level_value * 2
                            bottom_level = current_level_value * 0.1
                    elif ts == "Шорт":
                        if current_level_number + 1 == len(ld):
                            # bottom_level = current_level_value * 0.1
                            upper_level = current_level_value * 2
                else:
                    if current_level_number + 1 < len(levels):
                        upper_level = levels[current_level_number + 1]
                    else:
                        upper_level = current_level_value*2
                        # upper_level = current_level_value * 1.01
                    if current_level_number - 1 >= 0:
                        bottom_level = levels[current_level_number - 1]
                    else:
                        bottom_level = current_level_value * 0.1
                        # bottom_level = current_level_value * 0.99

                self.day_high = self.qs_num_three.day_high
                self.day_low = self.qs_num_three.day_low

                # Установка максимума и минимума дня
                Strategy.Functions.set_day_highlow(self)



                level_shots = self.qs_num_three.__dict__[level_name + "_shot"]

                # Цена пересекла уровень
                if candle_low < current_level_value < candle_high:
                    level_shots += 1
                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, level_name + "_shot",
                                                   self.qs_num_three.__dict__[level_name + "_shot"] + 1)

                    utl.Utility.otladka_print(
                                              txt=f"Цена каснулась ({self.qs_num_three.__dict__[level_name + '_shot'] + 1} раз) уровня {level_dict[level_name]}",
                                              lvl=4, ticker=ticker)

                    Strategy.Functions.strategy_num_three_delete_candles(self)

                    # if level_name == "resistance1" and level_shots == 1:
                    #     max_level =

                    # return False



                # book Цена ушла более чем на 0.9% от базового уровня в сторону сделки
                # if version == 2:
                if (ts == "Лонг" and self.day_high / level_in > (1 + 0.009)) or\
                    (ts == "Шорт" and self.day_low / level_in < (1 - 0.009)):
                    for _ in [
                              ['update_time', utl.Utility.current_utc_time()],
                              ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                                ['pass_reason', "Выключаю стратегию, т.к. Цена ушла более чем на 1,2% от базового уровня в сторону сделки"],
                                ['pass_reason_time', utl.Utility.current_utc_time()],
                                ['pass_reason_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                                ['pass_reason_last_price', candle_close]
                              ]:
                        dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                    return False

                # Цена ушла более чем на 0,9% от базового уровня в сторону сделки, в таком случае оставляем только базовый уровень и один уровень в сторону сделки
                # if step and min_level < 0 and self.day_low < level_in + step < self.day_high:
                # if level_name == "resistance1" and level_shots > 0 and min_level < 0:
                #     for _ in [
                #         ['min_level', 0],
                #         ['update_time', utl.Utility.current_utc_time()],
                #         ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))]
                #     ]:
                #         dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                #     min_level = 0
                #
                # if (ts == "Лонг" and self.day_high / level_in >= (1 + 0.009)) or\
                #     (ts == "Шорт" and self.day_low / level_in <= (1 - 0.009)):
                #
                #     if step:
                #         if ts == "Лонг":
                #
                #
                #     for _ in [
                #               ['update_time', utl.Utility.current_utc_time()],
                #               ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                #                 ['pass_reason', "Выключаю стратегию, т.к. Цена ушла более чем на 1,2% от базового уровня в сторону сделки"],
                #                 ['pass_reason_time', utl.Utility.current_utc_time()],
                #                 ['pass_reason_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                #                 ['pass_reason_last_price', candle_close]
                #               ]:
                #         dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                #     return False


                # new Если цена каснулась 1/4 уровня в сторону сделку от базового, то оставлять только базовый уровень и 1/4. Плюс цена должна находиться у базового уровня 25.04.23
                # if step and (\
                #         (ts == "Лонг" and max_level==1 and min_level<0 and day_low > (level_in-step) and day_high > (level_in+step)) or \
                #         (ts == "Шорт" and max_level==-1 and min_level>0 and day_high < (level_in+step) and day_low < (level_in-step))\
                #         ):
                #     for _ in [
                #         ["min_level", 0]
                #     ]:
                #         dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                #     min_level = 0


                # book Определение на каком уровне сейчас находится цена
                if (ts == "Лонг" and not (bottom_level < candle_close < current_level_value)) or\
                    (ts == "Шорт" and not (current_level_value < candle_close < upper_level)):
                    continue

                for _ in [
                    ['last_price', candle_close],
                    ['update_time', utl.Utility.current_utc_time()],
                    ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))]
                ]:
                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])

                # new Если цена ушла против сделки дальше минимального уровня, то? 25.04.23
                # if (ts == "Лонг" and current_level_number < min_level) or (ts == "Шорт" and current_level_number > min_level):
                #     pass

                # book Проверка на дальность уровня: Пропускаем уровень, так как он считается слишком далеким, так как цена сходила сейчас или до этого далеко против тренда
                if ts == "Лонг":
                    for key, value in level_names_dict.items():
                        if value == level_name:

                            # Переопределение нового максимального уровня
                            if key < 0 and key < max_level - 1:
                                max_level = key + 1
                                # print(f"max_level = {max_level}")
                                for _ in [
                                            ["max_level", max_level]
                                          ]:
                                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])

                            # Пропускаем уровень, так как он считается слишком далеким, так как цена сходила сейчас или до этого далеко против тренда
                            if key > max_level:
                                utl.Utility.otladka_print(
                                    txt=f"{rus_name} ({ticker}) Пропускаем уровень \"{level_dict[level_name]}\", так как он считается слишком далеким, так как цена сходила сейчас или до этого далеко против тренда",
                                    lvl=2,
                                    ticker=ticker)
                                Strategy.Functions.strategy_num_three_delete_candles(self)
                                Strategy.Functions.strategy_num_three_delete_level(self)
                                return False
                            break
                elif ts == "Шорт":
                    for key, value in level_names_dict.items():
                        if value == level_name:
                            # Переопределение нового максимального уровня
                            if key > 0 and key > max_level + 1:
                                max_level = key - 1
                                for _ in [["max_level", max_level]
                                          ]:
                                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                            # Пропускаем уровень, так как он считается слишком далеким, так как цена сходила сейчас или до этого далеко против тренда
                            if key < max_level:
                                utl.Utility.otladka_print(
                                    txt=f"{rus_name} ({ticker}) Пропускаем уровень \"{level_dict[level_name]}\", так как он считается слишком далеким, так как цена сходила сейчас или до этого далеко против тренда",
                                    lvl=2,
                                    ticker=ticker)
                                Strategy.Functions.strategy_num_three_delete_candles(self)
                                Strategy.Functions.strategy_num_three_delete_level(self)
                                return False
                            break
                    # if level_names_dict[]

                # Если цена больше 2ух раз каснулась уровня, то тогда пропускаем
                # TODO Если буду это использовать, то поменять обращение не к базе, а к переменной, так как она может менятся в ходе выполнении программы
                # if self.qs_num_three.__dict__[level_name + "_shot"] > 1 and cshet_kasaniy:
                #     utl.Utility.otladka_print(
                #                               txt=f"Цена каснулась ({self.qs_num_three.__dict__[level_name + '_shot']} раз) уровня {level_dict[level_name]}. Это предел. Идет распил уровня. Больше за этим уровнем не слежу.",
                #                               lvl=3, ticker=ticker)
                #     Strategy.Functions.strategy_num_three_delete_candles(self)
                #     Strategy.Functions.strategy_num_three_delete_level(self)
                #     return False

                # Присвоение названия первичного уровня
                if not self.qs_num_three.level_name:
                    utl.Utility.otladka_print(
                        txt=f"{rus_name} ({ticker}) Наблюдаю за первичным уровнем \"{level_dict[level_name]}\" со значением \"{current_level_value}\"", lvl=2,
                        ticker=ticker)
                    for _ in [["level_name", level_name],
                              ["level_value", current_level_value]
                              ]:
                        dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])

                # Изменился уровень
                if self.qs_num_three.level_name and self.qs_num_three.level_name != level_name:
                    # TODO добавить удаление лимтиной заявки (посмотреть в каких еще местах нужно это сделать)
                    utl.Utility.otladka_print(
                        txt=f"{rus_name} ({ticker}) Изменился уровень с \"{level_dict[self.qs_num_three.level_name]}\" на \"{level_dict[level_name]}\" со значением \"{current_level_value}\"",
                        lvl=2,
                        ticker=ticker)
                    Strategy.Functions.strategy_num_three_delete_candles(self)
                    Strategy.Functions.strategy_num_three_delete_level(self)
                    for _ in [["level_name", level_name],
                              ["level_value", current_level_value]
                              ]:
                        dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                    with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
                        self.qs_num_three = db.query(dbmain.DB_str_n_three).filter(
                            dbmain.DB_str_n_three.ticker == ticker,
                            dbmain.DB_str_n_three.date == utl.Utility.current_date(),
                            dbmain.DB_str_n_three.version == version
                        ).first()

                # Если уже было больше 3ех напоминаний от данного уровня
                # if self.qs_num_three.__dict__[level_name + '_reminder'] >= 3:
                #    utl.Utility.otladka_print(
                #        txt=f"У данного уровня уже было напоминание {self.qs_num_three.__dict__[level_name + '_reminder']} раз. Прекращаю напоминать от этого уровня",
                #        lvl=2, ticker=ticker)
                #    return False

                # Установка delta price
                if self.qs_num_three.type_signal == "Лонг":
                    delta_price = 100 * ((candle_close - current_level_value) / candle_close)
                elif self.qs_num_three.type_signal == "Шорт":
                    delta_price = 100 * (
                                (current_level_value - candle_close) / current_level_value)
                delta_price = float('{:.2f}'.format(delta_price))
                for _ in [['delta_price', delta_price]
                          ]:
                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])

                # Если цена ушла от ЛЮБОГО УРОВНЯ (пока не предусмотрен случай, если между уровнями больше чем 1,2%) больше чем на 1,2%, то в таком случае прекращаем стратегию
                # if delta_price <= -1.2:
                #     for _ in [
                #         ['update_time', utl.Utility.current_utc_time()],
                #         ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                #         ['pass_reason',
                #          "Выключаю стратегию, т.к. Цена ушла более чем на 1,2% от рассматриваемого уровня против сделки"],
                #         ['pass_reason_time', utl.Utility.current_utc_time()],
                #         ['pass_reason_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                #         ['pass_reason_last_price', candle_close]
                #     ]:
                #         dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                #     return False


                # Цена внутри канала включая границы 1ая свеча
                if (minute % 5 == 0 or stngs.Settings.Strategies.StrategiesMain.candle_period == 5) and not self.qs_num_three.candle_x1_name:
                    if (
                            ts == "Лонг" and base_border <= candle_high <= current_level_value and base_border <= candle_low <= current_level_value) or \
                            (
                                    ts == "Шорт" and  current_level_value <= candle_high <= base_border and current_level_value <= candle_low <= base_border)\
                            :
                        utl.Utility.otladka_print(
                            txt=f"Первый бар внутри канала около уровня \"{level_dict[level_name]}\" со значением \"{current_level_value}\"",
                            lvl=2, ticker=ticker)
                        for _ in [['candle_x1_name', level_name],
                                  ['candle_x1_value', current_level_value],
                                  ['candle_x1_last_price', candle_close],
                                  ['candle_x1_time', utl.Utility.current_utc_time()],
                                  ['candle_x1_minute', int(utl.Utility.current_utc_time().strftime("%M"))]
                                  ]:
                            dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                        return False

                # Цена внутри канала включая границы 2ая свеча
                # TODO поменять на minute % 5 == 4 когда буду снова использовать минутки
                if (minute % 5 == 4 or stngs.Settings.Strategies.StrategiesMain.candle_period == 5) and self.qs_num_three.candle_x1_name and not self.qs_num_three.candle_x2_name:

                    # Цена внутри канала включая границы
                    if (ts == "Лонг" and base_border <= candle_high <= current_level_value and base_border <= candle_low <= current_level_value) or \
                            (ts == "Шорт" and current_level_value <= candle_high <= base_border and current_level_value <= candle_low <= base_border)\
                            :
                        utl.Utility.otladka_print(
                            txt=f"Второй бар внутри канала \"{level_dict[level_name]}\" со значением \"{current_level_value}\".",
                            lvl=2, ticker=ticker)

                        type_round = {"Лонг": "🟢", "Шорт": "🔴"}
                        type_move = {"Лонг": "снизу-вверх 🔼", "Шорт": "сверху-вниз 🔽"}
                        type_move2 = {"Лонг": "Растет", "Шорт": "Падает"}
                        type_bolee = {"Лонг": "менее", "Шорт": "более"}
                        type_move_short = {"Лонг": "🔼", "Шорт": "🔽"}

                        # TODO Написать отклонение в процентах
                        msg = f"<b>{rus_name} ({ticker}) :: {self.qs_num_three.type_signal} {type_round[self.qs_num_three.type_signal]}</b>\n" \
                              f"<b>{versions_tlgm[version]}</b>\n\n" \
                              f"<b>Текущая цена: {candle_close} {type_move_short[self.qs_num_three.type_signal]}</b>\n" \
                              f"<u>{type_move2[self.qs_num_three.type_signal]}</u> к уровню: {self.qs_num_three.level_value}\n" \
                              f"____________________________\n" \
                              f"<i>Подготовьтесь к сделке в {self.qs_num_three.type_signal.lower()}.</i>\n" \
                              f"<i>Расчетный стоп-лосс: {float('{:.2f}'.format((self.qs_num_three.level_value * (1 + (0.003 * napr[self.qs_num_three.type_signal])))))}</i>\n"\
                              f"<i>* -0,3% от уровня пробития</i>"
                            # f"<i>Стоп-лосс обязателен.</i>\n\n" \
                            # f"<i>Стоп лосс не {type_bolee[self.qs_num_three.type_signal]}: {float('{:.2f}'.format((self.qs_num_three.level_value * (1 + (0.003 * napr[self.qs_num_three.type_signal])))))} (0,3% от уровня)</i>\n\n"

                        print(msg)

                        if not utl.Utility.send_msg_to_group(msg):
                            utl.Utility.otladka_print(
                                                      txt=f"🔴🔴🔴🔴 Торговый бот не смог отправить сообщение в телеграм",
                                                      lvl=0, ticker=ticker)

                        for _ in [['candle_x2_name', self.qs_num_three.level_name],
                                  ['candle_x2_value', current_level_value],
                                  ['candle_x2_last_price', candle_close],
                                  ['candle_x2_time', utl.Utility.current_utc_time()],
                                  ['candle_x2_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                                  [level_name + '_reminder', self.qs_num_three.__dict__[level_name + '_reminder'] + 1]
                                  ]:
                            dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])

                        obj_strategy_simulate_trading = trades.TradingSimulate()
                        obj_strategy_simulate_trading.main(ticker=ticker,
                                                           candle_close=candle_close,
                                                           candle_high=candle_high,
                                                           candle_low=candle_low,
                                                           rus_name=rus_name, minute=minute, start=1, strategy_name=strategy_name, version=version)

                        return False
                    elif (
                            ts == "Лонг" and candle_high <= current_level_value and candle_low < base_border) or \
                            (
                                    ts == "Шорт" and current_level_value <= candle_high <= base_border and candle_low > current_level_value) \
                            :
                        utl.Utility.otladka_print(
                            txt=f"Вторая свеча вышла за пределы коридора. Жду нового вхождения в коридор",
                            lvl=2, ticker=ticker)
                        Strategy.Functions.strategy_num_three_delete_candles(self)
                        return False

                # Вышла за пределы максимального АТР и обнуляем значения
                if (ts == "Лонг" and candle_low < base_out) or \
                        (ts == "Шорт" and candle_high > base_out)\
                        :
                    utl.Utility.otladka_print(
                        txt=f"Цена вне предельного коридора. Прекращаю следить за уровнем. Жду нового вхождения в коридор и нового уровня.",
                        lvl=3, ticker=ticker)

                    Strategy.Functions.strategy_num_three_delete_candles(self)
                    Strategy.Functions.strategy_num_three_delete_level(self)

                    # если это последний возможный уровень для стратегии плюс максимальное значение отклонения АТР, то выключаю стратегию
                    if (ts == "Лонг" and current_level_number == 0) or (ts == "Шорт" and current_level_number + 1 == len(ld)):
                        utl.Utility.otladka_print(
                            txt=f"Выключаю стратегию, т.к. Цена ушла на максимальное значение АТР от минимального уровня в обратную сторону сделки",
                            lvl=3, ticker=ticker)

                        for _ in [
                            ['update_time', utl.Utility.current_utc_time()],
                            ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                            ['pass_reason',
                             "Выключаю стратегию, т.к. Цена ушла на максимальное значение АТР от минимального уровня в обратную сторону сделки"],
                            ['pass_reason_time', utl.Utility.current_utc_time()],
                            ['pass_reason_minute', int(utl.Utility.current_utc_time().strftime("%M"))],
                            ['pass_reason_last_price', candle_close]
                        ]:
                            dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                        return False
                    return False

                # пересечение уровня
                if candle_low < current_level_value < candle_high:
                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, level_name + "_shot",
                                                   self.qs_num_three.__dict__[level_name + "_shot"] + 1)

                    utl.Utility.otladka_print(
                                              txt=f"Цена каснулась ({self.qs_num_three.__dict__[level_name + '_shot']+1} раз) уровня {level_dict[level_name]}",
                                              lvl=2, ticker=ticker)

                    Strategy.Functions.strategy_num_three_delete_candles(self)
                    return False
                return False
            # Цена ушла далеко от всех уровней. Прекращаю наблюдать за уровнями.
            else:
                utl.Utility.otladka_print(
                    txt=f"Цена ушла далеко от всех уровней. Прекращаю наблюдать за уровнями.",
                    lvl=3, ticker=ticker)
                Strategy.Functions.strategy_num_three_delete_candles(self)
                Strategy.Functions.strategy_num_three_delete_level(self)
                for _ in [
                          ["last_price", candle_close],
                        ['update_time', utl.Utility.current_utc_time()],
                        ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))]
                          ]:
                    dbscripts.db_update_cell_by_id(dbmain.DB_str_n_three, self.qs_num_three.id, _[0], _[1])
                return False

# class TradingSimulate:
#     def main(self, ticker, candle_close=0, rus_name="", start_time="", high=0, low=0, minute=None, start=0, strategy_name=""):
# 
#         # with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
#         #     qs_tickers_for_trading = db.query(dbmain.DB_str_n_three).filter(
#         #         dbmain.DB_str_n_three.candle_x2_name != None,
#         #         dbmain.DB_str_n_three.date == utl.Utility.current_date(),
#         #         dbmain.DB_str_n_three.ticker == ticker).first()
#         #
#         # with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
#         #     qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
#         #         dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
#         #         dbmain.DB_str_trading_simulate.ticker == ticker,
#         #         dbmain.DB_str_trading_simulate.stop_loss_value == None
#         #
#         #     ).first()
# 
#         utl.Utility.otladka_print(
#             txt=f"{rus_name} ({ticker}) Зашел на проверку симуляции торговли",
#             lvl=4,
#             ticker=ticker)
# 
#         if start == 1:
# 
#             utl.Utility.otladka_print(
#                 txt=f"{rus_name} ({ticker}) Получен сигнал на торговлю для выставления лимитной заявки",
#                 lvl=3,
#                 ticker=ticker)
# 
#             # Проверка на сигнал, который запустил стратегию
#             with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
#                 qs_str_n_three = db.query(dbmain.DB_str_n_three).filter(
#                     dbmain.DB_str_n_three.candle_x2_name != None,
#                     dbmain.DB_str_n_three.date == utl.Utility.current_date(),
#                     dbmain.DB_str_n_three.ticker == ticker).first()
# 
# 
#             # Проверка на то, есть ли уже запущенная стратегия, но не было входа. Если есть, то удаляю предыдущую не запущенную сделку
#             with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
#                 qs_ticker_for_trading_2 = db.query(dbmain.DB_str_trading_simulate).filter(
#                     dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
#                     dbmain.DB_str_trading_simulate.ticker == ticker,
#                     dbmain.DB_str_trading_simulate.trade_out_value == None,
#                     dbmain.DB_str_trading_simulate.trade_in_value == None
#                 ).first()
#             if qs_ticker_for_trading_2:
#                 utl.Utility.otladka_print(
#                     txt=f"{rus_name} ({ticker}) Есть уже запущенная стратегия, но не было входа. Удаляю предыдущую не запущенную сделку",
#                     lvl=3,
#                     ticker=ticker)
#                 db.delete(qs_ticker_for_trading_2)
#                 db.commit()
# 
#             # Проверка на работающуюу стратегию
#             with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
#                 qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
#                     dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
#                     dbmain.DB_str_trading_simulate.ticker == ticker,
#                     dbmain.DB_str_trading_simulate.trade_out_value == None,
#                     dbmain.DB_str_trading_simulate.trade_in_value != None
#                 ).first()
# 
#             # Если пришел сигнал на тот же уровень, но бот все еще находится в сделке по предыдущему сигналу
#             if qs_ticker_for_trading and qs_str_n_three.candle_x2_name and qs_ticker_for_trading.strategy_level_name \
#                     and qs_str_n_three.candle_x2_name == qs_ticker_for_trading.strategy_level_name \
#                     and qs_ticker_for_trading.trade_in_value != None \
#                     and qs_ticker_for_trading.trade_out_value == None:
#                 utl.Utility.otladka_print(
#                     txt=f"{rus_name} ({ticker}) Сигнал пришел сигнал на тот же уровень, но бот все еще находится в сделке по предыдущему сигналу.",
#                     lvl=3,
#                     ticker=ticker)
#                 return False
# 
#             # Если пришел сигнал на другой уровень, но бот все еще находится в сделке по предыдущему сигналу. То есть по более выгодному
#             # print(f"{qs_str_n_three.candle_x2_name}")
#             # print(qs_str_n_three.candle_x2_name != qs_ticker_for_trading.strategy_level_name)
#             # print(qs_ticker_for_trading.trade_in_value)
#             # print(qs_ticker_for_trading.trade_out_value)
# 
#             if qs_str_n_three.candle_x2_name and qs_ticker_for_trading \
#                     and qs_str_n_three.candle_x2_name != qs_ticker_for_trading.strategy_level_name \
#                     and qs_ticker_for_trading.trade_in_value \
#                     and not qs_ticker_for_trading.trade_out_value \
#                     :
#                 utl.Utility.otladka_print(
#                     txt=f"{rus_name} ({ticker}) Сигнал пришел на другой уровень, но бот все еще находится в сделке по предыдущему сигналу. То есть по более выгодному. Так что оставляю старую сделку.",
#                     lvl=3,
#                     ticker=ticker)
#                 return False
# 
#             # Зайти еще раз в сделку если по этому же уровню уже, так как ранее получил стоп лосс
#             if qs_str_n_three.candle_x2_name and qs_ticker_for_trading\
#                     and qs_str_n_three.candle_x2_name == qs_ticker_for_trading.strategy_level_name \
#                     and qs_ticker_for_trading.trade_in_value \
#                     and qs_ticker_for_trading.trade_out_value \
#                     :
#                 utl.Utility.otladka_print(
#                     txt=f"{rus_name} ({ticker}) Зашел еще раз в сделку если по этому же уровню уже, так как ранее получил стоп лосс.",
#                     lvl=3,
#                     ticker=ticker)
#                 pass
# 
#             if (
#                     qs_str_n_three.candle_x2_name and qs_ticker_for_trading \
#                     and qs_str_n_three.candle_x2_name == qs_ticker_for_trading.strategy_level_name \
#                     and qs_ticker_for_trading.trade_in_value \
#                     and qs_ticker_for_trading.trade_out_value \
#                     ) \
#                     or not qs_ticker_for_trading:
# 
#                 # if qs_ticker_for_trading:
#                 level_dict = {"level_in": "Базовый уровень", "resistance1": "Сопротивление 1",
#                               "resistance2": "Сопротивление 2", "support1": "Поддержка 1", "support2": "Поддержка 2"}
#                 utl.Utility.otladka_print(
#                     txt=f"{rus_name} ({ticker}) Добавление тикера для симуляции торговли от уровня \"{level_dict[qs_str_n_three.candle_x2_name]}\"",
#                     lvl=2,
#                     ticker=ticker)
#                 data = {}
# 
#                 data["date"] = utl.Utility.current_date()
#                 data["ticker"] = ticker
#                 data["create_time"] = utl.Utility.current_utc_time()
#                 data["type_signal"] = qs_str_n_three.type_signal
#                 data["strategy_name"] = strategy_name
#                 data["strategy_level_value"] = qs_str_n_three.candle_x2_value
#                 data["strategy_level_name"] = qs_str_n_three.candle_x2_name
#                 data["time_signal"] = qs_str_n_three.candle_x2_time
#                 data["last_price"] = candle_close
#                 data["update_time"] = utl.Utility.current_utc_time()
#                 data["update_minute"] = int(utl.Utility.current_utc_time().strftime("%M"))
# 
#                 if qs_str_n_three.type_signal == "Лонг":
#                     data["limit_value"] = float('{:.2f}'.format(qs_str_n_three.candle_x2_value * 1.001))
#                     data["stop_loss_value"] = float('{:.2f}'.format(data["limit_value"] * 0.997))
#                 elif qs_str_n_three.type_signal == "Шорт":
#                     data["limit_value"] = float('{:.2f}'.format(qs_str_n_three.candle_x2_value * 0.999))
#                     data["stop_loss_value"] = float('{:.2f}'.format(data["limit_value"] * 1.003))
# 
#                 with Session(autoflush=False, bind=engine) as db:
#                     tom = DB_str_trading_simulate(**data)
#                     db.add(tom)  # добавляем в бд
#                     db.commit()  # сохраняем изменения
# 
#                 with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
#                     qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
#                         dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
#                         dbmain.DB_str_trading_simulate.ticker == ticker).first()
# 
#         with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
#             qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
#                 dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
#                 dbmain.DB_str_trading_simulate.ticker == ticker,
#                 dbmain.DB_str_trading_simulate.trade_out_value == None
# 
#             ).first()
# 
#         # Если по тикеру нет никаких сделок
#         if not qs_ticker_for_trading:
#             return False
# 
#         # Если инструмент уже вышел из сделки
#         # if qs_ticker_for_trading.trade_out_time:
#         #     utl.Utility.otladka_print(
#         #         txt=f"{rus_name} ({ticker}) Инструмент уже вышел из сделки",
#         #         lvl=2,
#         #         ticker=ticker)
#         #     return False
# 
#         # Установка delta price
#         if qs_ticker_for_trading.type_signal == "Лонг":
#             delta_price = 100 * ((candle_close - qs_ticker_for_trading.limit_value) / candle_close)
#         elif qs_ticker_for_trading.type_signal == "Шорт":
#             delta_price = 100 * ((qs_ticker_for_trading.limit_value - candle_close) / qs_ticker_for_trading.limit_value)
#         delta_price = float('{:.2f}'.format(delta_price))
#         for _ in [['delta_price', delta_price],
#                   ['last_price', candle_close],
#                   ['update_time', utl.Utility.current_utc_time()],
#                   ['update_minute', int(utl.Utility.current_utc_time().strftime("%M"))]
#                   ]:
#             dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
# 
#         # Вход в сделку
#         if not qs_ticker_for_trading.trade_in_value:
#             if (high >= qs_ticker_for_trading.limit_value and qs_ticker_for_trading.type_signal == "Лонг") or\
#                 (low <= qs_ticker_for_trading.limit_value and qs_ticker_for_trading.type_signal == "Шорт")\
#             :
#                 utl.Utility.otladka_print(
#                     txt=f"{rus_name} ({ticker}) Вхожу в сделку на уровне {qs_ticker_for_trading.limit_value}",
#                     lvl=2,
#                     ticker=ticker)
# 
#                 type_round = {"Лонг": "🟢", "Шорт": "🔴"}
#                 type_move_short = {"Лонг": "🔼", "Шорт": "🔽"}
# 
#                 msg = f"<u>Вхожу в сделку в {qs_ticker_for_trading.type_signal} от уровня {qs_ticker_for_trading.limit_value}\n\n</u>"\
#                       f"<b>{rus_name} ({ticker}) :: {qs_ticker_for_trading.type_signal} {type_round[qs_ticker_for_trading.type_signal]}</b>\n\n" \
#                       f"<b>Текущая цена: {candle_close} {type_move_short[qs_ticker_for_trading.type_signal]}</b>" \
# 
# 
#                 # print(msg)
#                 #
#                 # if not utl.Utility.send_msg_to_group(msg):
#                 #     utl.Utility.otladka_print(
#                 #         txt=f"🔴🔴🔴🔴 Торговый бот не смог отправить сообщение в телеграм",
#                 #         lvl=0, ticker=ticker)
# 
# 
#                 for _ in [['trade_in_value', qs_ticker_for_trading.limit_value],
#                           ['trade_in_time', utl.Utility.current_utc_time()]
#                           ]:
#                     dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
#                 with tinkoffmain.Session(autoflush=False, bind=dbmain.engine) as db:
#                     qs_ticker_for_trading = db.query(dbmain.DB_str_trading_simulate).filter(
#                         dbmain.DB_str_trading_simulate.date == utl.Utility.current_date(),
#                         dbmain.DB_str_trading_simulate.ticker == ticker).first()
# 
#             # До сих пор не вошел в сделку
#             else:
#                 return False
# 
#         # Стоп лосс
#         if low <= qs_ticker_for_trading.stop_loss_value and qs_ticker_for_trading.type_signal == "Лонг":
#             utl.Utility.otladka_print(
#                 txt=f"{rus_name} ({ticker}) Стоп лосс {qs_ticker_for_trading.stop_loss_value} ({float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - qs_ticker_for_trading.stop_loss_value) / qs_ticker_for_trading.trade_in_value)))}%)",
#                 lvl=2,
#                 ticker=ticker)
# 
#             type_round = {"Лонг": "🟢", "Шорт": "🔴"}
#             type_move_short = {"Лонг": "🔼", "Шорт": "🔽"}
# 
#             msg = f"🔴 Стоп-лосс составил {float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - qs_ticker_for_trading.stop_loss_value) / qs_ticker_for_trading.trade_in_value)))}%" \
#                   f"<b>{rus_name} ({ticker}) :: {qs_ticker_for_trading.type_signal}</b>\n\n" \
#                   f"<b>Текущая цена: {candle_close} {type_move_short[qs_ticker_for_trading.type_signal]}</b>\n\n" \
#                   f"Стоп-лосс по сделке в {qs_ticker_for_trading.type_signal} от уровня {qs_ticker_for_trading.limit_value}\n"\
# 
# 
#             # print(msg)
#             #
#             # if not utl.Utility.send_msg_to_group(msg):
#             #     utl.Utility.otladka_print(
#             #         txt=f"🔴🔴🔴🔴 Торговый бот не смог отправить сообщение в телеграм",
#             #         lvl=0, ticker=ticker)
# 
#             for _ in [['trade_out_value', qs_ticker_for_trading.stop_loss_value],
#                       ['trade_out_time', utl.Utility.current_date()],
#                       ['percent_loss', float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - qs_ticker_for_trading.stop_loss_value) / qs_ticker_for_trading.trade_in_value)))]
#                       ]:
#                 dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
#             return False
#         elif high >= qs_ticker_for_trading.stop_loss_value and qs_ticker_for_trading.type_signal == "Шорт":
#             utl.Utility.otladka_print(
#                 txt=f"{rus_name} ({ticker}) Стоп лосс {qs_ticker_for_trading.stop_loss_value} ({float('{:.2f}'.format(100 * ((qs_ticker_for_trading.stop_loss_value - qs_ticker_for_trading.trade_in_value) / qs_ticker_for_trading.stop_loss_value)))}%)",
#                 lvl=2,
#                 ticker=ticker)
#             for _ in [['trade_out_value', qs_ticker_for_trading.stop_loss_value],
#                       ['trade_out_time', utl.Utility.current_date()],
#                       ['percent_loss', float('{:.2f}'.format(100 * ((qs_ticker_for_trading.stop_loss_value - qs_ticker_for_trading.trade_in_value) / qs_ticker_for_trading.stop_loss_value)))]
#                       ]:
#                 dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
#             return False
# 
#         # Сохранение максимально прибыльной цены
#         data = {}
#         if qs_ticker_for_trading.type_signal == "Лонг" and (
#                 (qs_ticker_for_trading.max_price and qs_ticker_for_trading.max_price < high) or
#                 not qs_ticker_for_trading.max_price
#         ):
#             utl.Utility.otladka_print(
#                 txt=f"{rus_name} ({ticker}) Зафиксировал максимальную прибыль {high} ({float('{:.2f}'.format(100 * ((high - qs_ticker_for_trading.trade_in_value) / high)))}%)",
#                 lvl=2,
#                 ticker=ticker)
#             for _ in [['max_price', high],
#                       ['percent_win', float('{:.2f}'.format(100 * ((high - qs_ticker_for_trading.trade_in_value) / high)))]
#                       ]:
#                 dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
#         elif qs_ticker_for_trading.type_signal == "Шорт" and (
#                 (qs_ticker_for_trading.max_price and low < qs_ticker_for_trading.max_price) or
#                 not qs_ticker_for_trading.max_price
#         ):
#             utl.Utility.otladka_print(
#                 txt=f"{rus_name} ({ticker}) Зафиксировал максимальную прибыль {low} ({float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - low) / qs_ticker_for_trading.trade_in_value)))}%)",
#                 lvl=2,
#                 ticker=ticker)
#             for _ in [['max_price', low],
#                       ['percent_win', float('{:.2f}'.format(100 * ((qs_ticker_for_trading.trade_in_value - low) / qs_ticker_for_trading.trade_in_value)))]
#                       ]:
#                 dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
# 
#         # Изменения стопа лосса в б/у, если цена ушла дальше +0,6%
#         if qs_ticker_for_trading.percent_win and qs_ticker_for_trading.percent_win >= 0.6 and qs_ticker_for_trading.stop_loss_value != qs_ticker_for_trading.limit_value:
#             utl.Utility.otladka_print(
#                 txt=f"{rus_name} ({ticker}) Изменения стопа в б/у, так как цена ушла дальше +0,6%",
#                 lvl=2,
#                 ticker=ticker)
#             for _ in [['stop_loss_value',  qs_ticker_for_trading.limit_value]
#                       ]:
#                 dbscripts.db_update_cell_by_id(dbmain.DB_str_trading_simulate, qs_ticker_for_trading.id, _[0], _[1])
#             return False
