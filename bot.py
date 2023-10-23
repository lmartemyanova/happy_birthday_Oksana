import os
from random import choice

from dotenv import load_dotenv, find_dotenv
import telebot
from telebot import types

load_dotenv(find_dotenv())

token = os.getenv('token')

bot = telebot.TeleBot(token)

help = """
Список команд: 
/help - показать информацию о командах 
/shit - навести порчу на говно
/show - показать список проклятых
/zero - обнулить список проклятых"""

shit_list = []
random_phrases = [
    "Пидорас обосрется!",
    "Будет срать дальше чем видеть!",
    "Жидкое неудержимое говно прольется в самый неподходящий момент!"
    "Ничто не поможет удержать говно внутри!"
]


def add_shit_item(name):
    if name.title() in shit_list:
        res = "Ты уже проклял(а) этого мерзкого пидора, но не переживай, я прокляну его еще раз для тебя *_*"
        return res
    else:
        shit_list.append(name.title())
        res = f"Готово, {name} проклят(а) на понос! {choice(random_phrases)}"
        return res


@bot.message_handler(commands=["start"])
def start_message(message):
    text_message = f"""
Привет, {message.from_user.first_name}!
Я навожу порчу на говно.
"""
    markup = types.ReplyKeyboardMarkup(True)
    button_start = types.KeyboardButton("Посмотреть список команд")
    markup.add(button_start)
    bot.send_message(message.chat.id, text_message, reply_markup=markup)


@bot.message_handler(commands=["help"])
def get_help(message):
    bot.send_message(message.chat.id, help)


@bot.message_handler(commands=["shit"])
def shit(message):
    sent = bot.send_message(message.chat.id, "Кого ты хочешь проклясть? Введи имя.")
    bot.register_next_step_handler(sent, doubleshit)


def doubleshit(message):
    name = message.text
    answer = add_shit_item(name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_help = types.KeyboardButton("/help")
    button_shit = types.KeyboardButton("/shit")
    button_show = types.KeyboardButton("/show")
    button_zero = types.KeyboardButton("/zero")
    markup.row(button_help, button_show, button_zero)
    markup.row(button_shit)
    bot.send_message(message.chat.id, answer, reply_markup=markup)


@bot.message_handler(commands=["show"])
def show(message):
    if len(shit_list) == 0:
        bot.send_message(message.chat.id, 'Вы пока никого не прокляли. Исправим?')
    else:
        shitted = "\n".join(shit_list)
        bot.send_message(message.chat.id, shitted)


@bot.message_handler(commands=["zero"])
def zero(message):
    shit_list.clear()
    bot.send_message(message.chat.id, "Грехи отпущены!")


@bot.message_handler(content_types=["text"])
def start_message(message):
    if message.text == "Посмотреть список команд":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_help = types.KeyboardButton("/help")
        button_shit = types.KeyboardButton("/shit")
        button_show = types.KeyboardButton("/show")
        button_zero = types.KeyboardButton("/zero")
        markup.row(button_help, button_show, button_zero)
        markup.row(button_shit)
        bot.send_message(message.chat.id, help, reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling()
