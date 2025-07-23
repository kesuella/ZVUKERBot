import logging
import json
import datetime
from telebot import TeleBot
from config import BOT_TOKEN
from auth import AuthManager

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bot.log'
)

bot = TeleBot(BOT_TOKEN)
auth_manager = AuthManager()
authorized_users = set()

def backup_settings():
    backup_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'authorized_users': list(authorized_users)
    }
    with open('backup.json', 'w') as f:
        json.dump(backup_data, f)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in authorized_users:
        send_auth_request(message)
    else:
        bot.send_message(message.chat.id, "Добро пожаловать!")

def send_auth_request(message):
    logging.info(f"Отправлен запрос на аутентификацию пользователю {message.from_user.id}")
    bot.send_message(
        message.chat.id,
        "Для доступа к боту необходимо настроить двухфакторную аутентификацию.\n"
        "Пожалуйста, отсканируйте QR-код с помощью приложения аутентификации."
    )
    qr_image = auth_manager.generate_qr()
    bot.send_photo(message.chat.id, qr_image)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я ZVUKERBot с поддержкой 2FA.\n"
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/help - показать эту справку\n"