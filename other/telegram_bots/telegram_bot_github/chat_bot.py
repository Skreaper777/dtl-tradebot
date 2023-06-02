"""

https://surik00.gitbooks.io/aiogram-lessons/content/chapter1.html

"""

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
print(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

@dp.message_handler()
async def echo_message(msg: types.Message):
    """
    #Объясняю, что мы только что написали: Если не указывать тип обрабатываемого сообщения, то библиотека по умолчанию делает обработку только текстовых сообщений - то, что нам и нужно. Поэтому скобки на первой строчке остаются пустыми.

    Параметр msg это всё то же сообщение, как и в предыдущих пунктах.

    В данном случае на последней строчке мы отправляем пользователю сообщение не ответом, а простым сообщением. Для этого мы воспользовались методом send_message и передали в него два обязательных параметра - айди чата, куда отправляем, и сам текст сообщения. Их мы взяли из объекта msg, который является представителем класса Message. Параметр from_user ссылается на ещё один объект - данный параметр имеет класс User. У него есть параметр id - уникальный идентификатор для чатов и каналов в телеграме. Ну и текст полученного сообщения мы получили из поля text.
    """
    await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)