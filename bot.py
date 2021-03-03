import logging, os

from aiogram import Bot, Dispatcher, executor, types
from client.EDAMTest import create_note
from utils import API_TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
session_storage = {
    'title': '',
    'text': ''
}


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['save'])
async def save_note(message: types.Message):
    create_note(session_storage['text'])
    await message.answer('note created')


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handle_docs_text(message: types.Message):
    try:
        photo = message.reply_to_message.photo
        text = message.reply_to_message.caption
    except:
        photo = message.photo
        text = message.caption
    session_storage['text'] = text
    await photo[-1].download()


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_docs_images(message):
    session_storage['text'] = message.text
    await message.answer(message)


# @dp.message_handler(content_types=[types.ContentType.ANY])
# async def handle(message: types.Message):
#     await message.answer(message)
#     if message.text and not message.reply_to_message.caption:
#         print(message.text)
#         create_note(message.text)
#     if message.text and message.reply_to_message.caption:
#         title = message.text
#         text = message.reply_to_message.caption
#         print(title, text)
#         [await photo.download() for photo in message.reply_to_message.photo]
#         create_note(text, title)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)