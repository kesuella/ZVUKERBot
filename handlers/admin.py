from aiogram import Router, types, F
from aiogram.filters import Command
from config import ADMINS
from database import get_pending_voices, approve_voice, delete_voice_by_file_id

router = Router()

@router.message(Command("moderate"))
async def show_pending(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("⛔ У тебя нет доступа.")
        return

    pending = await get_pending_voices()
    if not pending:
        await message.answer("Нет новых мемов на модерацию.")
        return

    for voice_id, keyword, file_id in pending:
        buttons = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="✅ Одобрить",
                    callback_data=f"approve:{keyword}:{file_id}"
                ),
                types.InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data="reject"
                )
            ]
        ])

        await message.bot.send_voice(
            chat_id=message.chat.id,
            voice=file_id,
            caption=f"🆕 Мем на модерации\nКлюч: <b>{keyword}</b>",
            reply_markup=buttons,
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("approve:"))
async def approve_callback(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMINS:
        await callback.answer("⛔ Недоступно", show_alert=True)
        return

    _, keyword, file_id = callback.data.split(":", 2)
    pending = await get_pending_voices()
    voice_id = next((vid for vid, kw, fid in pending if fid == file_id and kw == keyword), None)

    if voice_id is None:
        await callback.answer("❗ Мем уже обработан или не найден.")
        return

    await approve_voice(voice_id)
    await callback.message.edit_caption(
        f"✅ Мем одобрен!\nКлюч: <b>{keyword}</b>",
        parse_mode="HTML"
    )
    await callback.answer("✅ Одобрено!")

@router.callback_query(F.data == "reject")
async def reject_callback(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMINS:
        await callback.answer("⛔ Недоступно", show_alert=True)
        return

    file_id = callback.message.voice.file_id
    await delete_voice_by_file_id(file_id)

    await callback.message.edit_caption("❌ Мем отклонён и удалён из базы")
    await callback.answer("🗑 Удалено.")

