#!/usr/bin/python
# -*- coding:utf-8 -*-

import telebot
import base64
import sys
import re
import you_get
import logging
from time import sleep
from config import token
from os import chdir, system, rename

bot = telebot.TeleBot(token)

# debug
#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

# set default encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '您使用的是NM$L厂牌的专用bot')


def return_arg(str):
    'return arg from command'
    return str.split(" ", 1)[1]

def try_except(func):
    
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            bot.reply_to(args, '引发错误! 请确认自己没有输入错误的参数')

    return wrapper()


@bot.message_handler(commands=['b64encode'])
@try_except
def base64_encode(message):
    splited = return_arg(message.text)
    handled = base64.b64encode(splited)
    bot.reply_to(message, handled)

@bot.message_handler(commands=['b64decode'])
@try_except
def base64_decode(message):
    splited = return_arg(message.text)
    handled = base64.b64decode(splited)
    bot.reply_to(message, handled)

@bot.message_handler(commands=['cloudmusic'])
@try_except
def findall_cloudmusic_id(message):
    splited = return_arg(message.text)
    handled = re.findall('\d+', re.search('song.*userid?', splited).group())[0]
    copyable = '`%s`' % handled
    bot.reply_to(message, copyable, parse_mode="Markdown")
    #bot.send_message(message.chat.id, handled, parse_mode="Markdown")

@bot.message_handler(commands=['soundcloud'])
@try_except
def send_soundcloud(message):
    splited = return_arg(message.text)
    info = you_get.get_soundcloud_info(splited)
    title = info[1][1]
    title = title.replace(' ', '')
    Type = info[2][1].split()[0].lower()
    size = info[3][1]
    filename = title + "." + Type
    print filename

    msg = "正在下载" + title + "(" + size + ")"
    bot.reply_to(message, msg)

    chdir("/home/pi/github/bbs_bot/downloads/")
    system('you-get -O '+ '"' + title + '"' + " " + splited)

    dl_dir = '/home/pi/github/bbs_bot/downloads/' + filename
    music = open(dl_dir, 'rb')
    bot.send_audio(message.chat.id, music)

    sleep(5)
    system("rm *")


if __name__ == '__main__':
    bot.polling()

