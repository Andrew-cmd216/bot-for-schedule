import telebot
import main
from telebot import types
bot = telebot.TeleBot('8256246268:AAEeYE3pzceAoGn2MeAIqxw8apMaytwEfbw')

schedule = main.Schedule()
schedule.organise()

# Dictionary that stores the selected group for each user
user_groups = {}

@bot.message_handler(content_types=['text'])
def start(message):

    '''Function that starts the bot and sends group selection menu'''

    if message.text:
        get_group(message.chat.id)

def get_group(message):

    '''Function that sends inline buttons for group selection'''

    keyboard = types.InlineKeyboardMarkup()
    key_first = types.InlineKeyboardButton(text='23ФПЛ-1', callback_data='group_1')
    keyboard.add(key_first)
    key_second = types.InlineKeyboardButton(text='23ФПЛ-2', callback_data='group_2')
    keyboard.add(key_second)
    text = 'Из какой ты группы'
    bot.send_message(message, text=text, reply_markup=keyboard)

def get_day(message):

    '''Function that sends inline buttons for day selection'''

    keyboard = types.InlineKeyboardMarkup()
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for day in days:
        keyboard.add(types.InlineKeyboardButton(text=day, callback_data=day))
    text = 'Выбери день недели'
    keyboard.add(types.InlineKeyboardButton(text='Вернуться к выбору группы', callback_data='back_to_group'))
    bot.send_message(message, text=text, reply_markup=keyboard)

def get_back_button(message):

    '''Function that shows a single "Back to group selection" button '''

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Вернуться к выбору группы', callback_data='back_to_group'))
    bot.send_message(message, text='Вернуться в начало', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    '''Function that handles all callback button presses'''

    user_id = call.from_user.id

    # Group selection
    if call.data in ['group_1', 'group_2']:
        user_groups[user_id] = 1 if call.data == 'group_1' else 2
        get_day(call.message.chat.id)

    # Back to group selection
    elif call.data == 'back_to_group':
        get_group(user_id)
    # Day selection
    elif call.data in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        group = user_groups.get(user_id)
        if not group:
            bot.send_message(call.message.chat.id, "Пожалуйста, сначала выбери группу.", parse_mode='Markdown')
            get_group(call.message)
            return
        # Save the name of day of the week
        day_name = call.data
        # Get schedule text based on day and group
        if call.data == 'Понедельник':
            text = schedule.get_monday(group)
        elif call.data == 'Вторник':
            text = schedule.get_tuesday(group)
        elif call.data == 'Среда':
            text = schedule.get_wednesday(group)
        elif call.data == 'Четверг':
            text = schedule.get_thursday(group)
        elif call.data == 'Пятница':
            text = schedule.get_friday(group)
        elif call.data == 'Суббота':
            text = schedule.get_saturday(group)

        # Send schedule
        formatted_text = f"*{day_name}*\n{text}"
        bot.send_message(call.message.chat.id, formatted_text, parse_mode='Markdown')
        # Show "Back to group selection" button
        get_back_button(call.message.chat.id)

bot.polling(none_stop=True, interval=0)