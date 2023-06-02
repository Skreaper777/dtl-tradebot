import os
import time

from tinkoff.invest import (
    CandleInstrument,
    Client,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

TOKEN = 't.ue4Liz218jy7MmhLPltFo9hdOPjkBbLf-aahde1zvd9gYs0dLLPfZ-c7sylCbZabNV-FCvASPe9xBtwy7CejWg'
# TOKEN = 't.zSv0PvqY9KLK07vFsbvdjHAW0fh-qeN4TXr6PksjPJDUVdIkIFI0RZ-hhHHC2gMY7RHpDxnEcJlnWWmMQZztGg'


def main():
    def request_iterator():
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                waiting_close=True,
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    CandleInstrument(
                        figi="BBG004730N88",
                        interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,

                    )
                ],
            )
        )
        # yield MarketDataRequest(
        #     subscribe_candles_request=SubscribeCandlesRequest(
        #         waiting_close=True,
        #         subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
        #         instruments=[
        #             CandleInstrument(
        #                 figi="BBG00178PGX3",
        #                 interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
        #             ),
        #             CandleInstrument(
        #                 figi="BBG004730N88",
        #                 interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
        #             )
        #         ],
        #     )
        # )
        while True:
            time.sleep(1)

    with Client(TOKEN) as client:
        # iter = client.market_data_stream.market_data_stream(request_iterator())
        # print(f"Длина итератора = {*iter.__dict__}")
        # print(*iter)
        for marketdata in client.market_data_stream.market_data_stream(
                request_iterator()
        ):
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            # print(1111, marketdata, current_time)


            # print(f"marketdata.subscribe_info_response = {marketdata.subscribe_info_response}. ({current_time})")
            # print(f"РЕЗУЛЬТАТ\n{client.instruments.get_instrument_by(id_type=1, id=marketdata.candle.figi).instrument.ticker} ({current_time})")
            print(
                f"РЕЗУЛЬТАТ\n{marketdata} ({current_time})")


            if marketdata.subscribe_info_response:
                print(f"Зашел в break ({current_time})")
                break


if __name__ == "__main__":
    main()