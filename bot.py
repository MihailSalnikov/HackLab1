#/usr/bin/env python3

import os
import json
import telebot
import logging
import game
import action_tree
import utils
from telebot import types

# Define logging
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# Loading bot config
config = json.load(open("config.json"))

# Creating bot
bot = telebot.TeleBot(config['token'])

# Loading MDP nodes
nodes, start_message, help_message = utils.load_nodes('action_tree.yaml')

# Loading old user data
user_worlds = utils.load_worlds('data/user_worlds.json', nodes)
print(utils.dump_worlds(user_worlds))

@bot.message_handler(commands=['start', 'help', 'show_stats'])
def handle_start_help(message):
    logging.info(f"Chat id: {message.chat.id} | Message: {message.text}")
    if message.text == '/start':
        world = action_tree.World(nodes)
        user_worlds[message.chat.id] = world
        markup = types.ReplyKeyboardMarkup()
        for m in [action.message for action in world.possible_actions()]:
            markup.row(m)
        bot.send_message(message.chat.id, start_message)
        bot.send_message(message.chat.id, world.node.message, reply_markup=markup)
    elif message.text == '/help':
        bot.send_message(message.chat.id, help_message)
    elif message.text == '/show_stats':
        world = user_worlds.get(message.chat.id, action_tree.World(nodes))
        bot.send_message(message.chat.id, world.current_state)

@bot.message_handler(content_types=["text"])
def react_to_choice(message): # Название функции не играет никакой роли
    logging.info(f"Chat id: {message.chat.id} | Message: {message.text}")
    world = user_worlds.get(message.chat.id, action_tree.World(nodes))
    action_id = utils.get_action_id(world, message.text)
    try:
        assert action_id != -1, print(f"Something wrong in .yaml file; World: {world})")
        new_state, action_message = world.do_action(action_id)
    except Exception:
        pass
    markup = types.ReplyKeyboardMarkup()
    for m in [action.message for action in world.possible_actions()]:
        markup.row(m)
    user_worlds[message.chat.id] = world
    bot.send_message(message.chat.id, world.node.message, reply_markup=markup)
    # dumping progress
    # json.dump(utils.dump_worlds(user_worlds), open('data/user_worlds.json', 'w'))

if __name__ == '__main__':
     bot.infinity_polling()
