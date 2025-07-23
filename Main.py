# main.py
import logging
from aiogram import Bot, Dispatcher
from utils.config import load_config
from handlers import register_all_handlers
from database import Database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

def main():
    try:
        config = load_config()
        bot = Bot(token=config.bot.token)
        dp = Dispatcher(bot)
        
        # Инициализация базы данных
        db = Database()
        db.create_connection()
        db.create_tables()
        
        # Регистрация всех обработчиков
        register_all_handlers(dp)
        
        logging.info("Бот запущен")
        await dp.start_polling()
        
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}")
    finally:
        db.close_connection()
        logging.info("Соединение с БД закрыто")

if __name__ == '__main__':
    main()
