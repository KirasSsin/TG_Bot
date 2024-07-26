import os
import random
import config
import telebot # pip install telebot

from setup import bot, logger
from webhook import app
from telebot import types # pip install pyTelegramBotAPI

bot = telebot.TeleBot(config.token)


# --------------- dialog params -------------------
dialog = {
    'hello': {
        'in': ['привет', 'hello', 'hi', 'privet', 'hey'],
        'out': ['Здравствуйте']
             } 
         }


# --------------- bot -------------------
@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    logger.info(f'@{message.from_user.username} ({message.chat.id}) used /start or /help')
    bot.send_message(
        message.chat.id,
        '<b>Hello! This is a telegram bot template written by <a href="https://gitlab.goodsforecast.ru/myshak_kirill/TG_Bot">TGBot</a></b>',
        parse_mode='html'
    )


@bot.message_handler(func=lambda message: True)
def echo(message):
    for t, resp in dialog.items():
        if any(e in message.text.lower() for e in resp['in']):
            logger.info(f'@{message.from_user.username} ({message.chat.id}) used {t}:\n\n%s', message.text)
            bot.send_message(message.chat.id, random.choice(resp['out']))
            return

    logger.info(f'@{message.from_user.username} ({message.chat.id}) used echo:\n\n%s', message.text)
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    if os.environ.get("IS_PRODUCTION", "False") == "True":
        app.run()
    else:
        bot.infinity_polling()
