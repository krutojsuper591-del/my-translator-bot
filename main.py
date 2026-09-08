import os
from telebot import TeleBot
from translators import translate_text

# Бот будет брать токен из настроек сервера (секретов), чтобы это было безопасно
BOT_TOKEN = os.environ.get('BOT_TOKEN') 
bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне текст на русском, и я переведу его на английский. Или наоборот! 🇷🇺 ⇆ 🇬🇧")

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    text = message.text
    try:
        translated = translate_text(text, to_language='ru')
        if translated.lower().strip() == text.lower().strip():
            translated = translate_text(text, to_language='en')
        bot.reply_to(message, translated)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при переводе. Попробуйте еще раз.")

bot.infinity_polling()
