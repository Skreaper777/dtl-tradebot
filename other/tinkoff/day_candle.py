import logging
import os
from datetime import timedelta

from tinkoff.invest import CandleInterval
from tinkoff.invest.retrying.settings import RetryClientSettings
from tinkoff.invest.retrying.sync.client import RetryingClient
from tinkoff.invest.utils import now

# logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)

TOKEN = 't.ue4Liz218jy7MmhLPltFo9hdOPjkBbLf-aahde1zvd9gYs0dLLPfZ-c7sylCbZabNV-FCvASPe9xBtwy7CejWg'
retry_settings = RetryClientSettings(use_retry=True, max_retry_attempt=2)

with RetryingClient(TOKEN, settings=retry_settings) as client:
    result = []
    for candle in client.get_all_candles(
        figi="BBG004730N88",
        from_=now() - timedelta(days=1),
        # from_=now() - timedelta(hours=24),
        interval=CandleInterval.CANDLE_INTERVAL_DAY,
    ):
        result.append(candle)
    print(result[1])