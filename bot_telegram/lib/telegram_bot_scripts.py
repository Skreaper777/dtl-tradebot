import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def text_parser(data):
    data = data.lower()
    data = data.split("\n")
    ticker_dict = {"SBER": "Сбер", "SIBN": "Газпромнефть", "GAZP": "Газпром", "RUAL": "Русал", "TATNP": "Татнефтьпреф", "TATN": "Татнефть", "PHOR": "Фосагро",
                   "FIVE": "Х5", "YNDX": "Яша", "POLY": "Полик", "PLZL": "Полюс", "SNGSP": "СургутПреф", "SNGS": "Сургут",
                   "CHMF": "СС, cc, сс", "MAGN": "ММК", "ROSN": "Роснефть, Роснефь", "MTSS": "МТС", "AFLT": "Аэрофлот",
                   "MTLR": "Мечел", "TCSG": "Тинек", "OZON": "Озон", "ALRS": "Алроса", "GMKN": "ГМК", "NLMK": "НЛМК",
                   "LKOH": "Лукойл, лук", "NVTK": "Новатэк", "MGNT": "Магнит", "MOEX": "Сосбиржа, Мосбиржа", "VKCO": "ВК", "MVID": "Мвидео",
                   "AFKS": "АФК", "VTBR": "ВТБ", "UPRO": "Юнипро", "OGKB": "ОГК-2", "QIWI": "Киви", "HYDR": "Русгидро",
                   "IRAO": "Интеррао",

                   "SIM3": "Си, SI", "GDM3": "GD", "BRJ3": "BR", "MXM3": "МИХ", "NGH3": "NG", "SVM3": "SV", "EuM3": "EU",


                    "F": "F1", "GM" : "GM", "MSFT" : "MSFT", "CCL" : "CCL", "BYND" : "BYND", "AAPL" : "AAPL", "NVDA" : "NVDA",
                    "MRNA": "MRNA", "PLTR" : "PLTR", "ETSY" : "ETSY", "BMY" : "BMY", "KHC": "KHC", "MARA" : "MARA", "OKTA": "OKTA",
                   "NFLX": "NFLX", "SNAP": "SNAP", "CVX": "CVX", "DKNG": "DKNG", "PTON": "PTON", "MOMO": "MOMO", "TAL": "TAL", "TSLA": "TSLA",
                   "ATVI": "ATVI", "DAL": "DAL"

                   }

    temp_data = []
    global_query_lst = []

    for xi, x in enumerate(data):
        napr_sdelki = lvl_vhod = lomanaya_stroka = name_uroven1 = name_uroven2 = support1 = resistance1 = support2 = resistance2 = 0
        query_dict = {}
        if(xi) == 0:
            # temp_data.append([])

            # Установка даты
            date = x.split(".")
            if len(date) == 3:
                # print(111111)
                # temp_data.append([])
                # temp_data[-1].append(x)
                # query_dict['date'] = x
                # print(33333, query_dict)
                if len(date[2]) == 4:
                    date[2] = date[2][2:]
                date = '.'.join(date)
            else:
                # print(222222)
                # temp_data[-1].append("Без даты")
                # query_dict['date'] = "Без даты"
                date = "Без даты"
        else:

            for i, stroka in enumerate(x.split()):
                if not lomanaya_stroka:
                    if len(stroka)==1:
                        continue
                    stroka=stroka.lower()

                    if stroka[-1] == "." or stroka[-1] == ",":
                        stroka= stroka[:-1]
                    if stroka[0] == "." or stroka[0] == ",":
                       stroka = stroka[1:]

                    if set(stroka) < {'0','1','2','3','4','5','6','7','8','9','.',',','+'}:
                        try:
                            stroka = stroka.replace("+", "")
                            stroka = float(stroka.replace(",","."))

                        except:
                            pass

                    # Добавляю тикер и дату к нему
                    if i == 0:
                        for key, value in ticker_dict.items():
                            if str(value).lower().find(str(stroka).lower()) > -1:
                                temp_data.append([])
                                query_dict['ticker'] = key
                                query_dict['date'] = date
                        # else:
                        #     break

                    if query_dict.get('ticker'):
                        if stroka == "шорт" and not napr_sdelki:
                            temp_data[-1].append("Шорт")
                            query_dict['type_signal'] = "Шорт"
                            query_dict['max_level'] = -1
                            query_dict['min_level'] = 2
                            napr_sdelki = 1
                        elif stroka == "лонг" and not napr_sdelki:
                            temp_data[-1].append("Лонг")
                            query_dict['type_signal'] = "Лонг"
                            query_dict['max_level'] = 1
                            query_dict['min_level'] = -2
                            napr_sdelki = 1
                        # Неизвестно направление сделки
                        elif not napr_sdelki and not lvl_vhod and type(stroka) == float:
                            temp_data[-1].append("Неизвестно")
                            napr_sdelki = 1
                            lomanaya_stroka = 1
                        elif napr_sdelki and not lvl_vhod and type(stroka) == float:
                            temp_data[-1].append(float(stroka))
                            query_dict['level_in'] = float(stroka)
                            lvl_vhod = 1
                        elif napr_sdelki and lvl_vhod and type(stroka) != float and not name_uroven1:
                            if stroka == "под":
                                temp_data[-1].append("Поддержка")
                                name_uroven1 = 1
                                support1 = 1
                            elif stroka == "сопр":
                                temp_data[-1].append("Сопротивление")
                                name_uroven1 = 1
                                resistance1 = 1
                        elif name_uroven1 and type(stroka) == float and not name_uroven2:
                            temp_data[-1].append(float(stroka))
                            if support1:
                                if not query_dict.get('support1'):
                                    query_dict['support1'] = float(stroka)
                                else:
                                    query_dict['support2'] = float(stroka)
                            elif resistance1:
                                if not query_dict.get('resistance1'):
                                    query_dict['resistance1'] = float(stroka)
                                else:
                                    query_dict['resistance2'] = float(stroka)
                        elif name_uroven1 and type(stroka) != float and not name_uroven2:
                            if stroka == "под":
                                temp_data[-1].append("Поддержка")
                                support2 = 1
                                name_uroven2 = 1
                            elif stroka == "сопр":
                                temp_data[-1].append("Сопротивление")
                                resistance2 = 1
                                name_uroven2 = 1
                        elif name_uroven1 and type(stroka) == float and name_uroven2:
                            temp_data[-1].append(float(stroka))
                            if support2:
                                if not query_dict.get('support1'):
                                    query_dict['support1'] = float(stroka)
                                else:
                                    query_dict['support2'] = float(stroka)
                            elif resistance2:
                                if not query_dict.get('resistance1'):
                                    query_dict['resistance1'] = float(stroka)
                                else:
                                    query_dict['resistance2'] = float(stroka)
                        if type(stroka) == str and stroka.find("(") > -1 and stroka.find(")")>-1 and stroka[0]=="(":
                            stroka = stroka.replace(",", ".")
                            sopr = float(stroka[1:stroka.find(")")])
                            query_dict['step'] = sopr
                            temp_data[-1].append("Сопротивление")
                            temp_data[-1].append(sopr)

            else:
                if query_dict.get('ticker'):
                    global_query_lst.append(query_dict)

    return global_query_lst

def text_telegram_result(data):
    result_for_panda = []
    result_for_telegram = []
    for i, row in enumerate(data):
        delattr(row, '_sa_instance_state')
        result_for_panda.append(row.__dict__)
        result_for_telegram.append([])
        for x in row.__dict__.values():
            if x:
                result_for_telegram[i].append(x)
            else:
                result_for_telegram[i].append("-")
    return result_for_telegram, result_for_panda

def data_to_panda(data):
    temp_data_panda = pd.DataFrame.from_records(data, columns=["ticker", "date", "type_signal", "step", "level_in", "support1", "support2", "resistance1", "resistance2"])
    temp_data_panda = temp_data_panda.fillna(value="-")
    temp_data_panda.rename(columns={"ticker": "Тик", "date": "Дата", "type_signal": "Сиг", "step": "Шаг", "level_in": "Вход", "support1": "Под1", "support2": "Под2", "resistance1": "Соп1", "resistance2": "Соп2"}, inplace=True)
    return temp_data_panda