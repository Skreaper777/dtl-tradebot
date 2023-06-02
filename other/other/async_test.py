import asyncio
import os

from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    InfoInstrument,
    SubscriptionInterval,
)
from tinkoff.invest.async_services import AsyncMarketDataStreamManager

TOKEN = "t.ue4Liz218jy7MmhLPltFo9hdOPjkBbLf-aahde1zvd9gYs0dLLPfZ-c7sylCbZabNV-FCvASPe9xBtwy7CejWg"


async def main():
    async with AsyncClient(TOKEN) as client:
        market_data_stream: AsyncMarketDataStreamManager = (
            client.create_market_data_stream()
        )
        market_data_stream.candles.subscribe(
            [
                CandleInstrument(
                    figi="BBG004730N88",
                    interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                )
            ]
        )
        async for marketdata in market_data_stream:
            print(111, marketdata)
            market_data_stream.info.subscribe([InfoInstrument(figi="BBG000B9XRY4")])
            if marketdata.subscribe_info_response:
                print("STOP")
                market_data_stream.stop()


if __name__ == "__main__":
    asyncio.run(main())