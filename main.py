import os
from telebot import TeleBot
from translators import translate_text

# Вставляем токен прямо в код, чтобы не запутаться в настройках Koyeb
BOT_TOKEN = 8625622751:AAHDsCEX1wSI5mGbb-wa5A1TrUNy_TdgeyA 
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

