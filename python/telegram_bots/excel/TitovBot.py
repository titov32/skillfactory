import telebot
from config import *
from telebot import types

bot = telebot.TeleBot(TOKEN)
from extentions import printers, help_bot

fields = ['IP', 'Инвентарный номер', 'РМ', 'Местоположение']


def printer_markup(base=None):
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
    text = 'Для получения по принтерам нужно ввести номер Ланты сервис без нулей \
           поиск по серийнику в данный момент недоступен, напишите если он нужен'
    bot.reply_to(message, text)


@bot.message_handler(commands=['sn'])
def handle_start_help(message):
    text='данная команда в разработке, скажие Жеке и он легко ее реализует :-)  \
    а пока используйте номер Ланты'
    bot.reply_to(message, text)


def lanta_prossesing(message, number_lanta):
    if message.text in fields:
        inv = printers[number_lanta][message.text]
        bot.send_message(message.chat.id, f'{message.text}: {inv}')
        bot.send_message(message.chat.id, 'Выберите другую функцию или введите номер ланты', reply_markup=printer_markup(message.text))
        bot.register_next_step_handler(message, lanta_prossesing, number_lanta)
    else:
        bot.send_message(message.chat.id, f'такого номера нет')
        bot.send_message(message.chat.id, 'Можете использовать серийник через команду /sn')


@bot.message_handler(content_types=['text', 'audio'])
def handle_lanta(message):
    try:
        print(message)
        number_lanta = int(message.text)
        if message.chat.id in AUTH:
            bot.reply_to(message, f'Вы идентифицированы')
            bot.send_message(message.chat.id, f'Привет {message.chat.first_name} {message.chat.last_name}')
            if number_lanta in printers:
                bot.send_message(message.chat.id, 'Номер найден.')
                model = printers[number_lanta]['Модель']
                bot.send_message(message.chat.id, f'Модель принтера {model}', reply_markup=printer_markup())
                bot.register_next_step_handler(message, lanta_prossesing, number_lanta)
            else:
                bot.send_message(message.chat.id, f'такого номера нет')
                bot.send_message(message.chat.id, 'Можете использовать серийник через команду /sn')

        else:
            bot.send_message(message.chat.id, f'{message.chat.first_name} доступ запрещен, для доступа')
            bot.send_message(message.chat.id, f'Обратитесь к Жеке, ваш id {message.chat.id}')
            print('Пользователь без аунтицфикации')
            print(message.chat.username)
            print(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, help_bot)

bot.polling(non_stop = False)

