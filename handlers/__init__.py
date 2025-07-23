# handlers/__init__.py
from .tags import register_tags_handlers
from .audio import register_audio_handlers  # если есть обработчики загрузки аудио
from .other import register_other_handlers  # другие ваши обработчики

def register_all_handlers(dp: Dispatcher):
    register_tags_handlers(dp)
    register_audio_handlers(dp)  # раскомментируйте если используете
    register_other_handlers(dp)  # раскомментируйте если используете
