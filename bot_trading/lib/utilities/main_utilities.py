from decimal import Decimal
import time
import scripts.settings as stngs
import pytz
from datetime import datetime, timezone, timedelta
import telebot
import bot_trading.lib.db.db_scripts as dbscripts
from threading import Event

class Utility:
    @staticmethod
    def current_time():
        """
        Текущее время

        :return:
        """

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time

    @staticmethod
    def current_date():
        """
        Текущее время

        :return:
        """

        t = Utility.current_utc_time()
        t = t.strftime("%d.%m.%y")
        return t

    @staticmethod
    def current_utc_time():
        # now =
        # t = time.localtime()
        # current_utc_time = time.strftime("%Y:%m:%d %H:%M:%S", now)
        return datetime.now(timezone.utc)

    @staticmethod
    def current_time_offset(offset_in):
        offset = timedelta(hours=offset_in)
        tz = timezone(offset)
        dt = datetime.now()
        tz.utcoffset(dt)
        # print(dt)
        return dt

    @staticmethod
    def get_dif_time(t1, t2):
        # datetime1 = datetime.strptime("2023-03-17 10:15:02.191621+00:00", "%Y-%m-%d %H:%M:%S.%f%z")  # %Z%z

        # diftime = datetime.now(timezone.utc) - datetime1
        diftime = t1 - t2
        Utility.otladka_print(txt=f"Была запрошена разница во времени и она составляет = {diftime}", lvl=2)
        # print(diffe.total_seconds())

        return diftime

    @staticmethod
    def otladka_print(*args, **kwargs):
        kwargs.setdefault('end', '\n')
        kwargs.setdefault('lvl', 0)
        kwargs.setdefault('type_msg', 1)
        kwargs.setdefault('ticker', None)
        kwargs.setdefault('minute', None)

        if int(Utility.current_utc_time().strftime("%M")) % 5 == 0:
            minute_tw = int(Utility.current_utc_time().strftime("%M")) - 5
            if minute_tw < 0:
                minute_tw = 55
        else:
            minute_tw = -1


        data = {"text": kwargs['txt'], "update_time": Utility.current_utc_time(), "lvl": kwargs['lvl'],
                "date_ekb": Utility.current_time_offset(5).strftime("%d.%m.%y"),
                "time_ekb": Utility.current_time_offset(5).strftime("%H:%M:%S"),
                "ticker": kwargs['ticker'],
                "minute": int(Utility.current_utc_time().strftime("%M")),
                "minute_tw": minute_tw
                }

        dbscripts.db_insert_log(data)

        # остановка отладки
        if (kwargs['lvl'] and kwargs['lvl'] > stngs.Settings.Development.otladka_lvl) or not stngs.Settings.Development.otladka:
            return False
        # token = stngs.Settings.Telegram.stas_test_bot_token1
        # bot_trading = telebot.TeleBot(token)
        # chat_id = stngs.Settings.Telegram.stas_test_chatid1

        print(f"========= {kwargs['txt']} === ({Utility.current_time()})", end=kwargs['end'])

        # Utility.current_time_offset(5)
        # print(Utility.current_utc_time())

        # data = {"text": "1111", "update_time": Utility.current_utc_time, "lvl": kwargs['lvl'], "date_ekb": Utility.current_time_offset(5)}



        # with Session(autoflush=False, bind=engine) as db:
        #     tom = Log(**data)
        #     db.add(tom)  # добавляем в бд
        #     db.commit()  # сохраняем изменения


        # id = Column(Integer, primary_key=True, index=True)
        # update_time = Column(String)
        # date = Column(String)
        # text = Column(String)
        # lvl = Column(Integer)
        # date_ekb = Column(String)
        # time_ekb = Column(String)


        # if (kwargs['type_msg'] == 1):
        #     # bot_trading.send_message(chat_id, f"========= {kwargs['txt']} === Время: {Utility.current_time()}")
        #
        # elif (kwargs['type_msg'] == 2):
        #     print(f"========= {kwargs['txt']} === Время: {Utility.current_time()}", end=kwargs['end'])

    @staticmethod
    def convert_nano(x, y):
        return x + y / 1e9

    @staticmethod
    def convert_figi_to_ticker(figi):
        inv_d = {value: key for key, value in stngs.Settings.TinkoffApi.TickerFigi.figi_dict.items()}
        Utility.otladka_print(type_msg=2, txt=f"Конвертировал figi {figi} в название тикера {inv_d[figi]}", lvl=2)
        return inv_d[figi]

    @staticmethod
    def current_moscow_time():
        ct = datetime.now(pytz.timezone('Europe/Moscow'))
        Utility.otladka_print(txt=f"Текущее время {ct}", lvl=2)
        return ct

    @staticmethod
    def send_msg_to_group(msg):
        if stngs.Settings.Strategies.StrategiesMain.send_to_telegram:
            try:
                bot_trading, chat_id = Utility.tlgm_connecting_to_group()
                bot_trading.send_message(chat_id, f"{msg}", parse_mode="HTML")
                return True
            except:
                for _ in range(3):
                    try:
                        Event().wait(2)
                        bot_trading, chat_id = Utility.tlgm_connecting_to_group()
                        bot_trading.send_message(chat_id, f"{msg}", parse_mode="HTML")
                        return True
                    except:
                        return False
                    # https://stackoverflow.com/questions/68216439/python-telegram-bot-http-client-remotedisconnected-remote-end-closed-connection
                    # return False


    @staticmethod
    def tlgm_connecting_to_group():
        token = stngs.Settings.Telegram.current_bot
        bot_trading = telebot.TeleBot(token)
        chat_id = stngs.Settings.Telegram.current_chat
        return bot_trading, chat_id

class UtilityStratagies:
    @staticmethod
    def check_candle_by_minute(ccbm, H, M, candle, range=30):
        # print(1111, self.p_check_trading_only_at_session)
        if ccbm:
            if int(Utility.current_utc_time().strftime("%H")) == H and int(
                    Utility.current_utc_time().strftime("%M")) == M and int(
                    Utility.current_utc_time().strftime("%S")) <= range:
                return True
            else:
                Utility.otladka_print(
                    txt=f"Свеча {candle} не соответствует текущему времени {Utility.current_utc_time()}. Входящие параметры для свечи ={H}:{M}. Погрешность = {range} секунд",
                    lvl=2)
                return False
        else:
            return True

    @staticmethod
    def check_trading_only_at_session(trading_only_at_session):
        # Проверка на начало торговой сессии
        if trading_only_at_session:
            if int(Utility.current_utc_time().strftime("%H")) < 7 or int(Utility.current_utc_time().strftime("%H")) >= 16 or not 0 < int(
                Utility.current_utc_time().strftime("%w")) < 6 or (int(Utility.current_utc_time().strftime("%H")) == 7 and int(Utility.current_utc_time().strftime("%M")) <= 1):
                Utility.otladka_print(txt="Еще не началась торговая сессия. Бот ожидает начала торговой сессии", lvl=1)
                return False
            else:
                Utility.otladka_print(txt="Проверка на торговую сессию прошла успешно", lvl=3)
                return True
        else:
            return True

    @staticmethod
    def check_trading_period(trading_period=None):
        # Проверка на торговый период внутри сессии
        if trading_period:
            current_minute = int(Utility.current_utc_time().strftime("%H"))*60 + int(Utility.current_utc_time().strftime("%M"))
            time_left = int(trading_period[0].split(":")[0])*60 + int(trading_period[0].split(":")[1])
            time_right = int(trading_period[1].split(":")[0])*60 + int(trading_period[1].split(":")[1])
            if time_left <= current_minute <= time_right:
                Utility.otladka_print(txt="Проверка на период  внутри торговой сессии прошла успешно", lvl=5)
                return True
            else:
                Utility.otladka_print(txt="Торговый период внутри сессии для стратегии окончен", lvl=5)
                return False
        else:
            return True

class Files:
    def __init__(self, path, open_type):
        # self.open_file(path, open_type)
        self.path = path
        self.open_type = open_type

    def open_file(self, path, open_type):

        self.my_file = open(path, open_type, encoding="utf-8")
        # os.fsync(self.my_file.fileno())

        try:
            self.my_file = open(path, open_type, encoding="utf-8")
            # os.fsync(self.my_file.fileno())

            #### Отладка ####
            if stngs.Settings.Development.otladka:
                Utility.otladka_print(type_msg=2, txt="Файл успешно открыт", end="\n")
                pass

        except:
            raise "Невозможно открыть файл"

    def read_file(self):
        return self.my_file.read()

    def read_lines(self):
        with open(self.path, self.open_type, encoding="utf-8") as fw:
            return fw.readlines()
        # pass
        # return self.my_file.readlines()

    def write_file(self, txt):
        # self.my_file.write(txt+'\n')
        # self.my_file.flush()
        # self.close_file()

        # with open('foo.txt', 'w') as fp:
        #     fp.write(text)
        # self.my_file
        # db.create_data()
        with open(self.path, self.open_type, encoding="utf-8") as fw:
            fw.write(txt + '\n')
            fw.flush()
            # for line in lines:
            #     category = line[2]
            #     fw.write(category + '\n')

        #### Отладка ####
        # if stngs.Settings.Development.otladka:
        #     Utility.otladka_print(type_msg=2, txt="Файл успешно записан и закрыт", end="\n\n") if stngs.Settings.Development.otladka else None
        #     if stngs.Settings.Development.otladka_lvl2:
        #         # self.my_file = open(self.path, self.open_type, encoding="utf-8")
        #         print("Путь", self.path)
        #         Utility.otladka_print(type_msg=2, txt=f"В файл записана следующая информация = \"{txt}\"", end="\n\n")
        #         print(f"Вывожу содержимое файла ::::: Начало файла :::::: {open(self.path, 'r', encoding='utf-8').read()} :::::: Конец файла", end="\n\n")

    def close_file(self):
        self.my_file.close()

    # def parser_args():
    #     """
    #     Парсер входящих аргументов
    #     """
    #     # Парсер входящих параметров начало
    #     # parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    #     # parser.add_argument("--a", default=1, type=int, help="This is the 'a' variable")
    #     # args = parser.parse_args()
    #     # Парсер входящих параметров конец