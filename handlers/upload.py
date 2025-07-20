from aiogram import Router, types
from aiogram.filters import Command
from config import ADMINS
from database import add_voice
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("upload"))
async def ask_for_voice(message: types.Message):
    await message.answer("Пришли голосовое сообщение с подписью. Оно будет отправлено на модерацию.")

@router.message(lambda m: m.voice and m.caption)
async def handle_voice(message: types.Message):
    keyword = message.caption.strip().lower()
    file_id = message.voice.file_id
    user_id = message.from_user.id

    await add_voice(keyword, file_id, user_id)
    await message.reply("Спасибо! Мем отправлен на модерацию.")

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve:{keyword}:{file_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data="reject")
        ]
    ])

    for admin_id in ADMINS:
        await message.bot.send_voice(
            chat_id=admin_id,
            voice=file_id,
            caption=f"🆕 Мем на модерации\nКлюч: <b>{keyword}</b>",
            reply_markup=buttons,
            parse_mode="HTML"
        )