import telebot
from config import *
from telebot import types

bot = telebot.TeleBot(TOKEN)
from extentions import printers, help_bot

printer_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
printer_markup_btn1 = types.KeyboardButton('IP')
printer_markup_btn2 = types.KeyboardButton('Инвентарный номер')
printer_markup_btn3 = types.KeyboardButton('РМ')
printer_markup.add(printer_markup_btn1, printer_markup_btn2, printer_markup_btn3)


# Обрабатываются все сообщения содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, f'ответ на {message.text}')


@bot.message_handler(commands=['lanta'])
def handle_lanta(message):
    try:
        if message.chat.id in AUTH:
            bot.reply_to(message, f'Вы идентифицированы')
            bot.send_message(message.chat.id, 'введите номер ланты')
        else:
            bot.send_message(message.chat.id, f'Доступ запрещен, для доступа')
            bot.send_message(message.chat.id, f'Обратитесь к Жеке, ваш id {message.chat.id}')

    except ValueError:
        bot.reply_to(message, f'нужно ввести номер, а не что то другое и через пробел')
    bot.register_next_step_handler(message, lanta_info)


    def lanta_info(message):
    number_lanta = int(message.text)
    if number_lanta in printers:
        bot.send_message(message.chat.id, 'Номер найден.')
        model=printers[number_lanta]['Модель']
        bot.send_message(message.chat.id, f'Модель принтера {model}', reply_markup=printer_markup)
        print(message.text)
        bot.register_next_step_handler(message, lanta_prossesing, number_lanta)
    else:
        bot.send_message(message.chat.id, f'такого номера нет')
        print('Пользователь без аунтицфикации')
        print(message.chat.username)
        print(message.chat.id)


def lanta_prossesing(message, number_lanta):
    print(message.text)
    bot.send_message(message.chat.id, 'Что хотите узнать', reply_markup=printer_markup)
    if message.text=='IP':
        ip = printers[number_lanta]['IP']
        bot.send_message(message.chat.id, ip)
    elif message.text=='Инвентарный номер':
        inv = printers[number_lanta]['Инвентарный номер']
        bot.send_message(message.chat.id, inv)
    elif message.text == 'РМ':
        inv = printers[number_lanta]['РМ']
        bot.send_message(message.chat.id, inv)



def lanta_ip(message, number_lanta):
    ip = printers[number_lanta]['IP']
    bot.send_message(message.chat.id, ip)


def lanta_inv(message, number_lanta):
    inv = printers[number_lanta]['Инвентарный номер']
    bot.send_message(message.chat.id, inv)


def lana_rm(message, number_lanta):
    inv = printers[number_lanta]['РМ']
    bot.send_message(message.chat.id, inv)


@bot.message_handler(content_types=['text', 'audio'])
def handle_lanta(message):
    try:
        number_lanta=int(message.text)
        if message.chat.id in AUTH:
            bot.reply_to(message, f'Вы идентифицированы')
            bot.send_message(message.chat.id, f'Привет {message.chat.username}')
            if number_lanta in printers:
                bot.send_message(message.chat.id, 'Номер найден.')
                model = printers[number_lanta]['Модель']
                bot.send_message(message.chat.id, f'Модель принтера {model}', reply_markup=printer_markup)
                print(message.text)
                bot.register_next_step_handler(message, lanta_prossesing, number_lanta)
            else:
                bot.send_message(message.chat.id, f'такого номера нет')

        else:
            bot.send_message(message.chat.id, f'Доступ запрещен, для доступа')
            bot.send_message(message.chat.id, f'Обратитесь к Жеке, ваш id {message.chat.id}')
            print('Пользователь без аунтицфикации')
            print(message.chat.username)
            print(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, help_bot)



@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    bot.reply_to(message, f'Nice meme XDD')


bot.polling(none_stop=True)
