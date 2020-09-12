#/usr/bin/env python3

import json
import telebot


config = json.load(open("config.json"))

bot = telebot.TeleBot(config['token'])

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.infinity_polling()
