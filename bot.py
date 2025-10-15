import telebot
import main
from telebot import types
bot = telebot.TeleBot('8256246268:AAEeYE3pzceAoGn2MeAIqxw8apMaytwEfbw')

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text:
        get_day(message)

def get_day(message):
    keyboard = types.InlineKeyboardMarkup()
    key_monday = types.InlineKeyboardButton(text='Понедельник', callback_data='понедельник')
    keyboard.add(key_monday)
    key_tuesday = types.InlineKeyboardButton(text='Вторник', callback_data='вторник')
    keyboard.add(key_tuesday)
    key_wednesday = types.InlineKeyboardButton(text='Среда', callback_data='среда')
    keyboard.add(key_wednesday)
    key_thursday = types.InlineKeyboardButton(text='Четверг', callback_data='четверг')
    keyboard.add(key_thursday)
    key_friday = types.InlineKeyboardButton(text='Пятница', callback_data='пятница')
    keyboard.add(key_friday)
    key_saturday = types.InlineKeyboardButton(text='Суббота', callback_data='суббота')
    keyboard.add(key_saturday)
    text = 'Выбери день недели'
    bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'понедельник':
        bot.send_message(call.message.chat.id, main.Schedule.get_monday(1))
    elif call.data == 'вторник':
        bot.send_message(call.message.chat.id, main.Schedule.get_tuesday(1))
    elif call.data == 'среда':
        bot.send_message(call.message.chat.id, main.Schedule.get_wednesday(1))
    elif call.data == 'четверг':
        bot.send_message(call.message.chat.id, main.Schedule.get_thursday(1))
    elif call.data == 'пятница':
        bot.send_message(call.message.chat.id, main.Schedule.get_friday(1))
    elif call.data == 'суббота':
        bot.send_message(call.message.chat.id, main.Schedule.get_saturday(1))

bot.polling(none_stop=True, interval=0)