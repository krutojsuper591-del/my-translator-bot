import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telebot import TeleBot
from translators import translate_text

# --- Код фальшивого веб-сервера для бесплатного тарифа Render ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Запускаем веб-сервер в отдельном потоке
threading.Thread(target=run_web_server, daemon=True).start()
# --------------------------------------------------------------

# --- Сам бот-переводчик ---
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
