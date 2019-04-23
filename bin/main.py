#!/usr/bin/python3
# -*- coding:utf-8 -*-

import telebot
import base64
import sys
import re
import you_get
import logging
from time import sleep
from config import token
import os

bot = telebot.TeleBot(token)

# debug
#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

# set default encoding to utf-8
#sys.setdefaultencoding('utf-8')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '您使用的是NM$L厂牌的专用bot')


def return_arg(str):
    'return arg from command'
    return str.split(" ", 1)[1]

def try_except(message):
    def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except:
                    bot.reply_to(message, '引发错误! 请确认自己没有输入错误的参数')
            return wrapper
    return decorator

@try_except
@bot.message_handler(commands=['b64encode'])
def base64_encode(message):
    splited = return_arg(message.text)
    handled = base64.b64encode(splited.encode())
    bot.reply_to(message, handled)

@try_except
@bot.message_handler(commands=['b64decode'])
def base64_decode(message):
    splited = return_arg(message.text)
    handled = base64.b64decode(splited.encode())
    bot.reply_to(message, handled)

@try_except
@bot.message_handler(commands=['cloudmusic'])
def findall_cloudmusic_id(message):
    splited = return_arg(message.text)
    handled = re.findall('\d+', re.search('song.*userid?', splited).group())[0]
    copyable = '`%s`' % handled
    bot.reply_to(message, copyable, parse_mode="Markdown")
    #bot.send_message(message.chat.id, handled, parse_mode="Markdown")

@try_except
@bot.message_handler(commands=['soundcloud'])
def send_soundcloud(message):
    dl_dir = "/home/pi/github/bbs_bot/downloads/"
    if os.path.exists(dl_dir):
        pass
    else:
        os.makedirs(dl_dir)

    os.chdir(dl_dir)
    os.system("rm *")

    splited = return_arg(message.text)
    info = you_get.get_soundcloud_info(splited)
    title = info[1][1]
    title = title.replace(' ', '')
    Type = info[2][1].split()[0].lower()
    size = info[3][1]
    filename = title + "." + Type
    #print filename

    msg = "正在下载" + title + "(" + size + ")"
    bot.reply_to(message, msg)

    os.system('you-get ' + splited)


    dl_dir = '/home/pi/github/bbs_bot/downloads/' + filename
    files = os.listdir('/home/pi/github/bbs_bot/downloads/')
    osfilename = files[0]
    music = open(osfilename, 'rb')
    bot.send_audio(message.chat.id, music)

    sleep(5)
    os.system("rm *")


from nmsl_local import text_to_emoji as nmsl
@try_except
@bot.message_handler(commands=['nmsl'])
def nmslwsngg(message):
    splited = return_arg(message.text)
    text_with_emoji = nmsl(splited, 0)
    copyable = '`%s`' % text_with_emoji
    bot.reply_to(message, copyable, parse_mode="Markdown")


if __name__ == '__main__':
    bot.polling()

