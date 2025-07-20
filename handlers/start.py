from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Напиши /upload и пришли голосовой мем с подписью. Он отправится на модерацию.")