import time
from datetime import datetime, timezone
# TIME_FORMAT='%Y-%m-%d %H:%M:%S'
# ts = int(time.time()) # UTC timestamp
# timestamp = datetime.utcfromtimestamp(ts).strftime(TIME_FORMAT)
# d1 = datetime.strptime(timestamp + "+0000", TIME_FORMAT + '%z')
# ts1 = d1.timestamp()
# print("Time as string : %s" % d1)
# print("Source timestamp : %d" % ts)
# print("Parsed timestamp : %d" % ts1)


# 2023-03-17 10:15:02.191621+00:00
#
# import scripts.settings as stngs
# import pytz
# from datetime import datetime, timezone
# import telebot
#
# print(datetime.now(timezone.utc) - datetime("2023-03-17 10:15:02.191621+00:00").strftime('%Y/%m/%d %H:%M:%S.%f'))


# time = "%Y-%m-%d %H:%M:%S %Z%z"


# datetime1 = datetime.strptime("2023-03-17 10:15:02.191621", "%Y-%m-%d %H:%M:%S.%f") #%Z%z
# datetime1 = datetime.strptime("2023-03-17 10:15:02.191621+00:00", "%Y-%m-%d %H:%M:%S.%f%z") #%Z%z
#
# diffe = datetime.now(timezone.utc)-datetime1
#
# print(diffe.total_seconds())


print(datetime.now(timezone.utc).strftime("%H:%M:%S"))