import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Основные настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

# Настройки 2FA
SECRET_KEY = os.getenv('SECRET_KEY')  # Секретный ключ для TOTP
TOTP_URI = None  # URI для QR-кода

# Настройки базы данных (для хранения пользователей)
DB_FILE = 'users.db'
