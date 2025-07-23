# handlers/tags.py
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from database import Database
from models import AudioTrack

db = Database()

def register_tags_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['tag'])
    async def tag