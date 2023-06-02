import logging

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '6277870580:AAGpkjQJZYL11vwzRQUsQFCxYytZ0DPPIc0'


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)