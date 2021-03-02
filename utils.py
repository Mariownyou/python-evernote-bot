import os

from dotenv import load_dotenv


load_dotenv()
API_TOKEN = os.getenv('telegram_token')
EVERNOTE_TOKEN = os.getenv('evernote_token')

def list_folder():
    arr = os.listdir('photos')
    return arr 

def delete_files():
    files = list_folder()
    for file in files:
        os.remove('photos/' + file)
        