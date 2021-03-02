import logging, os

from aiogram import Bot, Dispatcher, executor, types
from client.EDAMTest import create_note
from utils import API_TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


# @dp.message_handler(content_types=['caption', 'photo', 'text'])
# async def handle_docs_text(message):
#     if message.text and not message.caption:
#         print(message.text)
#         create_note(message.text)
#         return
#     print(message.caption)
#     await message.answer(message)
#     await message.photo[-1].download()
#     create_note(message.caption)


@dp.message_handler(content_types=[types.ContentType.ANY])
async def handle(message: types.Message):
    await message.answer(message)
    if message.text and not message.reply_to_message.caption:
        print(message.text)
        create_note(message.text)
    if message.text and message.reply_to_message.caption:
        title = message.text
        text = message.reply_to_message.caption
        print(title, text)
        [await photo.download() for photo in message.reply_to_message.photo]
        create_note(text, title)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)