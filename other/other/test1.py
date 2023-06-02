import os

my_file = open("../../bot/txt/test1.txt", "r", encoding="utf-8")
os.fsync(my_file.fileno())