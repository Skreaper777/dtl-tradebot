import telebot

token = '6277870580:AAGpkjQJZYL11vwzRQUsQFCxYytZ0DPPIc0'
bot = telebot.TeleBot(token)
chat_id = '-1001842806326'
text = 'Hello python'
bot.send_message(chat_id, text)