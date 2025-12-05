from flask import Flask, request
import telebot
import time

TOKEN = '8283521307:AAG_dLTIx4cY1WiG4WNr6t9af07sKBcmvxw'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'ok', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот работает через вебхук на Render")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Главная защита — не отвечать на свои сообщения и старьё
    if message.from_user.is_bot:
        return
    if message.date < int(time.time()) - 60:
        return
    
    bot.reply_to(message, message.text)

@app.route('/')
def index():
    return "Бот живой!"

if __name__ == '__main__':
    app.run()
