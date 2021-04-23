import telebot
from config import *
from telebot import types
from extensions import Converter
bot = telebot.TeleBot(TOKEN)


def val_markup(base=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for field in fields:
        if field != base:
            buttons.append(types.KeyboardButton(field))

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
    pass

def lanta_prossesing(message, number_lanta):
    if message.text in fields:
        inv = printers[number_lanta][message.text]
        bot.send_message(message.chat.id, f'{message.text}: {inv}')
        bot.send_message(message.chat.id, 'Выберите другую функцию или введите номер ланты', reply_markup=printer_markup(message.text))
        bot.register_next_step_handler(message, lanta_prossesing, number_lanta)
    else:
        bot.send_message(message.chat.id, f'такого номера нет')
        bot.send_message(message.chat.id, 'Можете использовать серийник через команду /sn')




bot.polling(non_stop = False)