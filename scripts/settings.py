class Settings:
    class TinkoffApi:
        class Token:
            stas_sandbox = 't.ue4Liz218jy7MmhLPltFo9hdOPjkBbLf-aahde1zvd9gYs0dLLPfZ-c7sylCbZabNV-FCvASPe9xBtwy7CejWg'
            stas_main = 't.zSv0PvqY9KLK07vFsbvdjHAW0fh-qeN4TXr6PksjPJDUVdIkIFI0RZ-hhHHC2gMY7RHpDxnEcJlnWWmMQZztGg'

        class Account_id:
            stas_sandbox = 'a9d1b0b4-af34-44e9-b556-9ee9fa82d511'

        class TickerFigi:
            sber_figi = 'BBG004730N88'
            aapl_figi = 'BBG000B9XRY4'
            vkco_figi = 'BBG00178PGX3'
            figi_dict = {'SBER': sber_figi, 'AAPL': aapl_figi, 'VKCO': vkco_figi}

        class Settings:
            # candle_period = 5
            pass

    class Development:
        otladka = 1
        # tinkoff_start = 1
        # otladka_lvl2 = 1
        otladka_lvl = 9

    class Telegram:
        stas_test_bot_token1 = '6277870580:AAE906tLUqlQOGnTlUK1eWo-WLBoTfyNPiE' # старый 6277870580:AAGpkjQJZYL11vwzRQUsQFCxYytZ0DPPIc0
        stas_bot_predboyevoy_token = '6174636331:AAE-HdtzlxhMD-hsu0_I8qyYgxa1czjoJBM'
        stas_weatherbot_token = '6128619632:AAF0evAyz2QPtFLdbhLSpSZRGV1MVHrL7gA'
        stas_test_chatid1 = '-1001842806326'
        stas_chatid1_predboyevoy = '-1001630830705'

        current_bot = stas_bot_predboyevoy_token # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        current_chat = stas_chatid1_predboyevoy # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    class Strategies:
        class StrategiesMain:
            send_to_telegram = 1 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            tinkoff_start = 1 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            candle_period = 5 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        class Strategy_num_one_settings:
            trading_only_at_session = 0
            dif_between_query = 1 #50 по умолчанию для одной минуты, для 5ти минут 240 секнуд
            check_candle_by_minute = 0

        class Strategy_num_two_settings:
            trading_only_at_session = 0 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            dif_between_query = 1  # 50 по умолчанию для одной минуты, для 5ти минут 240 секнуд
            check_candle_by_minute = 0
            sbros_stratefii_atr_out = 1
            sbros_stratefii_atr_max = 0.6
            sbros_stratefii_atr_min = 0.4

        class Strategy_num_three_settings:
            trading_only_at_session = 0 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            trading_period = ["7:01", "9:00"] # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # trading_period = ["13:01", "20:00"]
            # trading_period = ["0:01", "20:00"]
            # dif_between_query = 1  # 50 по умолчанию для одной минуты, для 5ти минут 240 секнуд
            # check_candle_by_minute = 0
            sbros_stratefii_atr_out = 1.2
            sbros_stratefii_atr_high = 0.35
            sbros_stratefii_atr_low = 0.3
            cshet_kasaniy = 0