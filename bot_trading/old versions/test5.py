import sys
sys.path.append("C:/Users/stasr/PycharmProjects/trading-bot/venv/Lib/site-packages")

import os
# import logging
from datetime import datetime
from decimal import Decimal
import time

import telebot

from tinkoff.invest import (
    CandleInstrument,
    Client,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
    MoneyValue
)

from tinkoff.invest.utils import decimal_to_quotation, quotation_to_decimal


# TOKEN = os.environ["INVEST_TOKEN"]
# TOKEN = 't.zSv0PvqY9KLK07vFsbvdjHAW0fh-qeN4TXr6PksjPJDUVdIkIFI0RZ-hhHHC2gMY7RHpDxnEcJlnWWmMQZztGg' # Реальный токен
TOKEN = 't.ue4Liz218jy7MmhLPltFo9hdOPjkBbLf-aahde1zvd9gYs0dLLPfZ-c7sylCbZabNV-FCvASPe9xBtwy7CejWg' # Токен для песочницы

# logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
# logger = logging.getLogger(__name__)


def add_money_sandbox(client, account_id, money, currency="rub"):
    """Function to add money to sandbox account."""
    money = decimal_to_quotation(Decimal(money))
    return client.sandbox.sandbox_pay_in(
        account_id=account_id,
        amount=MoneyValue(units=money.units, nano=money.nano, currency=currency),
    )

def send_msg(txt):
    # t = time.localtime()
    # current_time = time.strftime("%H:%M", t)

    token = '6277870580:AAGpkjQJZYL11vwzRQUsQFCxYytZ0DPPIc0'
    bot = telebot.TeleBot(token)
    chat_id = '-1001842806326'
    bot.send_message(chat_id, txt)
    print(txt)


send_msg("Начало программы")

class Main():
    "Подписка на стрим минутных свечей и их вывод examples/stream_client.py"


    def request_iterator(self):
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                waiting_close=True,
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    CandleInstrument(
                        # figi="BBG00178PGX3", #VKCO
                        figi="BBG000B9XRY4", # AAPL
                        interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                    )
                ],
            )
        )
        while True:
            time.sleep(1)


    def start(self):
        with Client(TOKEN) as client:



            sandbox_accounts = client.sandbox.get_sandbox_accounts()
            # print("Вот все счета в песочнице", sandbox_accounts)

            account_id = sandbox_accounts.accounts[0].id
            # a9d1b0b4-af34-44e9-b556-9ee9fa82d511
            # print(account_id)

            print(
                "money: ",
                float(
                    quotation_to_decimal(
                        client.sandbox.get_sandbox_positions(account_id=account_id).money[0]
                    )
                ),
            )

            # print(add_money_sandbox(client=client, account_id=account_id, money=-3900000))



            for marketdata in client.market_data_stream.market_data_stream(
                self.request_iterator()
            ):
                # print(marketdata)
                try:
                    vhod_v_sdelku_long = 486.4
                    vhod_v_sdelku_short = 485.8

                    t = time.localtime()
                    current_time = time.strftime("%H:%M", t)

                    lst_data = float(str(marketdata.candle.close.units) + '.' + str(marketdata.candle.close.nano)[:2])
                    send_msg(f"========= Последняя котировка: {lst_data} === Время: {current_time}")

                    if lst_data > vhod_v_sdelku_long:
                        send_msg(f"вхожу в сделку на лонг === Время: {current_time}")
                    elif lst_data < vhod_v_sdelku_short:
                        send_msg(f"вхожу в сделку на лонг === Время: {current_time}")

                except:
                    send_msg(f"========= Еще не пришло === Время: {current_time}")


obj1 = Main()
obj2 = Main()

obj1.start()
obj2.start()


print(obj1.__dict__)