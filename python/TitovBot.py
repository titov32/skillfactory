import telebot
from config import *
from telebot import types
bot = telebot.TeleBot(TOKEN)

printer_markup = types.ReplyKeyboardMarkup()
printer_markup_btn1 = types.KeyboardButton('инфо')
printer_markup_btn2 = types.KeyboardButton('ремонт')
printer_markup.add(printer_markup_btn1, printer_markup_btn2)

# Обрабатываются все сообщения содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, f'ответ на {message.text}')

@bot.message_handler(commands=['lanta'])
def handle_lanta(message):
    try:
        if message.chat.id in AUTH:
            bot.reply_to(message, f'Вы аунтифициорованы')
            bot.send_message(message.chat.id, 'введите номер ланты')
        else:
            bot.send_message(message.chat.id, f'Доступ запрещен, для доступа')
            bot.send_message(message.chat.id, f'Обратитесь к администратору группы, ваш id {message.chat.id}')

    except ValueError:
        bot.reply_to(message, f'нужно ввести номер, а не что то другое и через пробел')
    bot.register_next_step_handler(message, lanta_info)

def lanta_info(message):
    number_lanta = int(message.text)
    bot.send_message(message.chat.id, 'Что хотите узнать', reply_markup = printer_markup)
    if number_lanta in lanta:
        bot.send_message(message.chat.id, f'инфо по {number_lanta}')
        text=f'серийник {lanta[number_lanta]} '
        bot.send_message(message.chat.id, text)
        print(*lanta[number_lanta])
    else:
        bot.send_message(message.chat.id, f'такого номера нет')

# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['text', 'audio'])
def handle_docs_audio(message):
    bot.send_message(message.chat.id, f'Hi {message.chat.username}')
    print(message.chat.username)
    print((message))

@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    bot.reply_to(message, f'Nice meme XDD')



bot.polling(none_stop=True)