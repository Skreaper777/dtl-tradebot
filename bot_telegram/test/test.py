ticker_dict = {"SBER": "Сбер", "GAZP": "Газпром", "RUAL": "Русал", "TATN": "Татнефть", "PHOR": "Фосагро", "FIVE": "Х5", "YNDX": "Яша"}

str = "Сбер лонг 176, под 175. 174. Сопр 150, ,151,450 \n  Газпром Шорт 161, под 160.  \nРусал лонг 41, под 40,75.  \nТатнефть лонг 340, под 335.  \nФосагро лонг 7030, под 7000. - \nХ5 лон 1500, пробой.  \nЯша лонг 1900, под 1880."



def text_parser(data):
    # print("Начал выполнять", data)
    data = data.split("\n")
    temp_data = []
    for xi, x in enumerate(data):
        temp_data.append([])
        napr_sdelki = 0
        lvl_vhod = 0
        lomanaya_stroka = 0
        name_uroven1 = 0
        name_uroven2 = 0
        for i, y in enumerate(x.split()):
            if not lomanaya_stroka:
                y = y.lower()
                if y[-1] == "." or y[-1] == ",":
                    y = y[:-1]
                if y[0] == "." or y[0] == ",":
                    y = y[1:]
                # print(set(y))
                if set(y) < {'0','1','2','3','4','5','6','7','8','9','.',','}:

                    y = float(y.replace(",","."))
                if i == 0:
                    for key, value in ticker_dict.items():
                        if value.lower().find(y.lower()) > -1:
                            temp_data[xi].append(key)
                elif y == "шорт" and not napr_sdelki:
                    temp_data[xi].append("Шорт")
                    napr_sdelki = 1
                elif y == "лонг" and not napr_sdelki:
                    temp_data[xi].append("Лонг")
                    napr_sdelki = 1
                elif not napr_sdelki and not lvl_vhod and type(y) == float:
                    temp_data[xi].append("Неизвестно")
                    napr_sdelki = 1
                    lomanaya_stroka = 1
                elif napr_sdelki and not lvl_vhod and type(y) == float:
                    temp_data[xi].append(float(y))
                    lvl_vhod = 1
                elif napr_sdelki and lvl_vhod and type(y) != float and not name_uroven1:
                    if y == "под":
                        temp_data[xi].append("Поддержка")
                        name_uroven1 = 1
                    elif y == "сопр":
                        temp_data[xi].append("Сопротивление")
                        name_uroven1 = 1
                elif name_uroven1 and type(y) == float:
                    temp_data[xi].append(float(y))
                elif name_uroven1 and type(y) != float and not name_uroven2:
                    if y == "под":
                        temp_data[xi].append("Поддержка")
                        name_uroven2 = 1
                    elif y == "сопр":
                        temp_data[xi].append("Сопротивление")
                        name_uroven2 = 1

                    # print(temp_data)
        # for y in x.split():
    # print("done", temp_data)
    return temp_data




print(text_parser(str))