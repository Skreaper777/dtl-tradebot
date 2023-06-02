# from datetime import datetime, timezone, timedelta
# from datetime import datetime, timedelta
#
# clock_in_half_hour = datetime.now() + timedelta(minutes=30)
#
# print(clock_in_half_hour)
# sec = datetime.now(timezone.utc)
# print(sec + timedelta(minutes=30))



# print(14%5)
# print(5%5)



# trading_period = ["16:00", "17:30"]
# h = 17
# m = 31
# if (h >= int(trading_period[0].split(":")[0]) and m >= int(trading_period[0].split(":")[1])) and (h <= int(trading_period[1].split(":")[0]) and m <= int(trading_period[1].split(":")[1])):
#     print(1)
# else:
#     print(0)
#
#
# def check(stime):
#     minutes, seconds = stime.split(':')
#     seconds = int(seconds) + (int(minutes) * 60)
#     return seconds <= (59 * 60)
#
#
# # using
# print(check('9:00'))
# print(check('59:00'))
# print(check('59:01'))
# print(check('109:00'))

x = "05.04.2023"
y = "2023"
date = x.split(".")
if len(date) == 3:
    # print(111111)
    # temp_data.append([])
    # temp_data[-1].append(x)
    # query_dict['date'] = x
    # print(33333, query_dict)
    print(date[2][2:])
    if len(date[2]) == 4:
        date[2] = y[-1:-2]

    date = '.'.join(date)
    print(date)