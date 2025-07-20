from aiogram import Router, types
from aiogram.types import InlineQueryResultVoice
from database import search_voices

router = Router()

@router.inline_query()
async def handle_inline(inline_query: types.InlineQuery):
    query = inline_query.query.strip().lower()
    voices = await search_voices(query)

    results = [
        InlineQueryResultVoice(
            id=str(i),
            title=f"Мем: {query}",
            voice_file_id=file_id
        )
        for i, (file_id,) in enumerate(voices)
    ]

    await inline_query.answer(results[:10], cache_time=1)