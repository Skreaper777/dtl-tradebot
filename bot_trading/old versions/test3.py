import sys
sys.path.append("C:/Users/stasr/PycharmProjects/trading-bot/venv/Lib/site-packages")

import os
import time

import telebot

from tinkoff.invest import (
    CandleInstrument,
    Client,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

# TOKEN = os.environ["INVEST_TOKEN"]
# TOKEN = 't.zSv0PvqY9KLK07vFsbvdjHAW0fh-qeN4TXr6PksjPJDUVdIkIFI0RZ-hhHHC2gMY7RHpDxnEcJlnWWmMQZztGg' # Реальный токен
TOKEN = 't.ue4Liz218jy7MmhLPltFo9hdOPjkBbLf-aahde1zvd9gYs0dLLPfZ-c7sylCbZabNV-FCvASPe9xBtwy7CejWg' # Токен для песочницы



def send_msg(txt):
    # t = time.localtime()
    # current_time = time.strftime("%H:%M", t)

    token = '6277870580:AAGpkjQJZYL11vwzRQUsQFCxYytZ0DPPIc0'
    bot = telebot.TeleBot(token)
    chat_id = '-1001842806326'
    bot.send_message(chat_id, txt)
    print(txt)


send_msg("Начало программы")

def main():
    "Подписка на стрим минутных свечей и их вывод examples/stream_client.py"

    def request_iterator():
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                waiting_close=True,
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    CandleInstrument(
                        figi="BBG00178PGX3",
                        interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                    )
                ],
            )
        )
        while True:
            time.sleep(1)

    with Client(TOKEN) as client:
        for marketdata in client.market_data_stream.market_data_stream(
            request_iterator()
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


if __name__ == "__main__":
    main()