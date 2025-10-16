import telebot
import main
from telebot import types
bot = telebot.TeleBot('8256246268:AAEeYE3pzceAoGn2MeAIqxw8apMaytwEfbw')

schedule = main.Schedule()
schedule.organise()

user_groups = {}

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text:
        get_group(message)

def get_group(message):
    keybord = types.InlineKeyboardMarkup()
    key_first = types.InlineKeyboardButton(text='23ФПЛ-1', callback_data='group_1')
    keybord.add(key_first)
    key_second = types.InlineKeyboardButton(text='23ФПЛ-2', callback_data='group_2')
    keybord.add(key_second)
    text = 'Из какой ты группы'
    bot.send_message(message.from_user.id, text=text, reply_markup=keybord)

def get_day(message):
    keyboard = types.InlineKeyboardMarkup()
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for day in days:
        keyboard.add(types.InlineKeyboardButton(text=day, callback_data=day))
    text = 'Выбери день недели'
    bot.send_message(message, text=text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = call.from_user.id

    if call.data in ['group_1', 'group_2']:
        user_groups[user_id] = 1 if call.data == 'group_1' else 2
        get_day(call.message.chat.id)

    elif call.data in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        group = user_groups.get(user_id)
        if not group:
            bot.send_message(call.message.chat.id, "Пожалуйста, сначала выбери группу.", parse_mode='Markdown')
            get_group(call.message)
            return
        if call.data == 'Понедельник':
            bot.send_message(call.message.chat.id, schedule.get_monday(group), parse_mode='Markdown')
        elif call.data == 'Вторник':
            bot.send_message(call.message.chat.id, schedule.get_tuesday(group), parse_mode='Markdown')
        elif call.data == 'Среда':
            bot.send_message(call.message.chat.id, schedule.get_wednesday(group), parse_mode='Markdown')
        elif call.data == 'Четверг':
            bot.send_message(call.message.chat.id, schedule.get_thursday(group), parse_mode='Markdown')
        elif call.data == 'Пятница':
            bot.send_message(call.message.chat.id, schedule.get_friday(group), parse_mode='Markdown')
        elif call.data == 'Суббота':
            bot.send_message(call.message.chat.id, schedule.get_saturday(group), parse_mode='Markdown')

bot.polling(none_stop=True, interval=0)