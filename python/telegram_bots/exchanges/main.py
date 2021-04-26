import telebot
from config import *
from telebot import types
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)


def val_markup(base=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in exchanges:
        if val != base:
            buttons.append(types.KeyboardButton(val))

    markup.add(*buttons)
    return markup


# Обрабатываются все сообщения содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = 'Этот бот для конвертации валют, для запуска используйте команду /convert \
            для получения списка валют используйте команду /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def handle_value(message):
    val = ''
    for i in exchanges:
        val += i.upper() + ' '
    bot.send_message(message.chat.id, f'Доступные валюты {val}. \
    Для конвертации используюйте команду /convert')


@bot.message_handler(commands=['convert'])
def handle_convert_from(message):
    text = 'Выберите валюту для конвертации'
    bot.send_message(message.chat.id, text, reply_markup=val_markup())
    bot.register_next_step_handler(message, handle_convert_to)


def handle_convert_to(message):
    base=message.text.lower()
    text = 'Выберите валюту в которую конвертировать'
    bot.send_message(message.chat.id, text, reply_markup=val_markup(base))
    bot.register_next_step_handler(message, handle_convert_amount, base)


def handle_convert_amount(message, base):
    quote=message.text.lower()
    text = 'Напишите сумму денег для конвертации'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, handle_convert_convert, base, quote)


def handle_convert_convert(message, base, quote):
    amount=message.text
    try:
        text=Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации /n {e}')
    else:
        bot.send_message(message.chat.id, text)



bot.polling()
