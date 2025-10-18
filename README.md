# bot-for-schedule
## USER MANUAL

Target audience
The instruction is intended for students of groups 23FPL-1 and 23FPL-2, as well as teachers. They can use a bot to plan the school day on a daily basis.

Purpose of the documentation
Provide headstart to working with the bot. The document should prevent typical errors and reduce support requests by giving clear step-by-step instructions.

Context of use
Students contact the bot via Telegram to check the schedule before classes. The relevance of the data and the simplicity of the interface are important. The bot solves the problem of searching schedules in different sources and provides a single reliable one.

Schedule Chat Bot

GET STARTED
Open chat with the bot in Telegram (username - @fipl_schedulebot);
Bot activates by pressing the “Start” button or writing anything.

SELECT GROUP
Press button “23ФПЛ-1” or “23ФПЛ-2”;
Bot will remember your choice.

SELECT DAY OF WEEK
Press button with required day:
- “Понедельник” - “Вторник” - “Среда”
- “Четверг” - “Пятница” - “Суббота”
Use `Вернуться к выбору группы` to return to group selection.

RECEIVE SCHEDULE
Read schedule in format:
```
14:40-16:00
Французский язык гр 2
Мазанова М.А.
Ауд.103
ул. Костина 2Б
```
Pay attention to the possible presence of dates that indicate the changes, or the period of lectures and seminars. 

HELPFUL INFO
Look for bold text - times and classrooms highlighted for convenience;
Read carefully - multiple subjects at the same time separated by empty lines;
Remember addresses - bot displays full names of the buildings.

TROUBLESHOOTING
Check Internet connection;
Restart bot - send “/start”.



## Technical Interface Documentation

1. MODULE “main.py”

1.1. CLASS “Schedule”
Purpose: Main schedule management class

Public methods:

Initialization and data loading:

schedule = Schedule()              # Create instance
schedule.organise()                # Load data from Google Sheets

Getting schedules:

schedule.get_monday(1) → str  # Monday for group 1
schedule.get_tuesday(2) → str  # Tuesday for group 2  
schedule.get_wednesday(1) → str  # Wednesday for group 1
schedule.get_thursday(2) → str  # Thursday for group 2
schedule.get_friday(1) → str  # Friday for group 1
schedule.get_saturday(2) → str  # Saturday for group 2


Parameters:
“group_id”: 1 (23ФПЛ-1) or 2 (23ФПЛ-2)
Returns: formatted schedule string

1.2. CLASS “DayOfTheWeek”
Purpose: Single day data processing

Methods:

day = DayOfTheWeek(dataframe)      # Create day from DataFrame
day.get_data(1) → DataFrame  # Get data for group
day.transform_data(2) → None       # Transform to text (result in day.table)


---

2. MODULE “bot.py”

MAIN FUNCTIONS

Message handler:
start(message) → None              # Launch bot on any message

Show selection interface:
get_group(message) → None          # Show group selection
get_day(chat_id) → None            # Show day selection

Button handler:
callback_worker(call) -> None       # Handle button press


BUTTONS AND CALLBACK_DATA
Group selection:
“23ФПЛ-1” → “callback_data=’group_1’”
“23ФПЛ-2” → “callback_data='group_2'”

Day selection:
“Monday” → “callback_data='Понедельник'”;
“Tuesday” → “callback_data='Вторник'”;
 ... (similarly for all days)

GLOBAL VARIABLES

bot = TeleBot('TOKEN')              # Bot instance
schedule = Schedule()               # Schedule instance  
user_groups = {}                    # State storage: {user_id: group_id}





## PYTHON CODE OVERVIEW
The Python code for chatbot is divided into two parts:
main.py
bot.py

1) MAIN.PY
This part details core functions used by the bot.
The code uses Pandas, GSpread and Google.Oauth2 libraries. For the sake of project a full access Google table duplicating the official HSE HSF schedule Google table (https://docs.google.com/spreadsheets/d/1UZ5pbRFI_qZbBOxCaJLTR3TYVSxkwPdL_w5Hm4j3Ytw/edit?gid=99866231#gid=99866231) was created and parsed via Google API (for further information please consult the following documentation: https://console.developers.google.com). Setting up Pandas requires outlining paths to the project and credentials.json file (featuring host-specific data), as well as presenting API URLs as the scope.
The function make_req is used in order for the program to get access to table data. The function reads the table using client.open().get.worksheet() method, then returns pandas.DataFrame class object with its values.
The part features following classes:
DayOfTheWeek (DotW) - features protected data attributes subset (pandas.DataFrame) and table (string); subset is preset, starting value for table is None. Uses the following methods:
_get_data(self, group_id: int) - assigns table value to the parsed table segment corresponding to the presented group_id (1 for 23FaAL-1 group, 2 for 23FaAL-2 group)
transform_data(self, group_id: int) - alters the data received via _get_table function to make it easier to perceive. Examples include:
changing campus acronyms to building addresses;
renaming columns;
removing extra symbols used in original table (eg. /n).
Following that the table variable is transformed into a dictionary using the .to.dict() method. Then all non-empty lines have their subjects separated (should they feature more than one per time period) and combined with corresponding auditories. The results are added to a new list - table_final, which is then transformed into a string object and has its value assigned to table attribute.   
get_schedule - returns table string. 
Schedule - features attributes df (pandas.DataFrame), monday/tuesday/wednesday/thursday/friday/saturday (DayOfTheWeek); starting value for all attributes is None. Uses the following methods:
fill_the_table - sets df value to a result of make_req function.
_make_monday (_make_tuesday, etc) - creates DayOfTheWeek class instance from table lines with fitting indexes and assigns its value to the corresponding attribute.
organize - this function is called after creating Schedule class object to fill its attributes using fill_the_table and _make… functions.
get_monday (get_tuesday, etc) - executes transform_data(group_id) and get_schedule functions for the chosen attribute 

2) BOT.PY
	This part details the way the bot operates and its UI.
	The code uses Telebot library and main.py file. 
The bot is initialized by creating a telebot.Telebot(tag) object with an individual tag; then the Schedule class object is created and has organize function called. Finally, an empty user groups dictionary is created. After defining all functions the bot is launched by .polling() method.
The part features following functions:
start - bot initialization, triggered after sending a message or pressing ‘Start’ button. Executes get_group function (see below).
get_group - creates a group selection message with two callback-triggering options for a user. 
get_day - creates a day selection message with seven callback-triggering options for a user (six for days and ‘Return to group selection’). 
get_back_button - adds an option allowing user to return to group selection after retrieving the schedule.
callback_worker - this function processes callbacks after choosing options. Includes:
assigning group IDs in correspondence with user input (1 for 23FaAL-1 group, 2 for 23FaAL-2 group), followed by executing get_day function;
returning to group selection should this be requested by user;
retrieving a schedule for a selected day in accordance with user group_id and sending it as a formatted string along with the day of the week.
