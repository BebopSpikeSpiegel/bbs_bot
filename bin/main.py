#!/usr/bin/python
# -*- coding:utf-8 -*-

import telebot
import base64
import sys
from config import token
bot = telebot.TeleBot(token)

# set default encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '您使用的是NM$L厂牌的专用bot')


def return_arg(str):
    'return arg from command'
    return str.split()[1]

@bot.message_handler(commands=['b64encode'])
def base64_encode(message):
    try:
        splited = return_arg(message.text)
        handled = base64.b64encode(splited)
        bot.reply_to(message, handled)
    except:
        bot.reply_to(message, '引发错误! 请确认自己没有输入错误的参数')

@bot.message_handler(commands=['b64decode'])
def base64_decode(message):
    try:
        splited = return_arg(message.text)
        handled = base64.b64decode(splited)
        bot.reply_to(message, handled)
    except:
        bot.reply_to(message, '引发错误! 请确认自己没有输入错误的参数')


def keep_running():
    try:
        bot.polling()
    except:
        bot.keep_running()

if __name__ == '__main__':
    keep_running()

