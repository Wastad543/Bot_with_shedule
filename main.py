import datetime

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor

from BD import conn_to_bd
from BD import know_week

bot = Bot(token='2111238592:AAEyrQcTj0lKhx3YNlwga4uF2xVxx0GITw4', parse_mode="HTML")
dp = Dispatcher(bot)

choose_markup = ReplyKeyboardMarkup(resize_keyboard=True)
choose_markup.row("Schedule for today")
choose_markup.row("Schedule for any day")

daytime_markup = ReplyKeyboardMarkup(resize_keyboard=True)
daytime_markup.row("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
daytime_markup.row("Change week", "Back")

numero_week = know_week()

@dp.message_handler(commands=['start'])
@dp.message_handler(regexp="Back")
async def start(message):
    await message.answer("Hello. Let's see the schedule for today or not? For more info you should write /help", reply_markup=choose_markup)


@dp.message_handler(regexp="Schedule for today")
async def today_table(message):
    day = datetime.datetime.today().strftime('%A')

    total_timetable = conn_to_bd(know_week(), day)

    await message.answer(total_timetable)


@dp.message_handler(regexp="Schedule for any day")
async def custom_table(message):
    await message.answer("You can make a choice", reply_markup=daytime_markup)


@dp.message_handler(regexp="Monday")
@dp.message_handler(regexp="Tuesday")
@dp.message_handler(regexp="Wednesday")
@dp.message_handler(regexp="Thursday")
@dp.message_handler(regexp="Friday")
async def upper_table(message):
    msg_text = message.text
    total_timetable = conn_to_bd(numero_week, msg_text)
    await message.answer(total_timetable)

@dp.message_handler(regexp="Change week")
async def change_week(message):
    global numero_week
    if numero_week=='Chetnaya':
        numero_week='Nechetnaya'
    else:
        numero_week='Chetnaya'

    await message.answer('Week was changed')

# Команды
@dp.message_handler(commands=['week'])
async def what_week(message):
    await message.answer(know_week()+' week')

@dp.message_handler(commands=['mtuci'])
async def link_mtuci(message):
    await message.answer('https://mtuci.ru/')

@dp.message_handler(commands=['help'])
async def get_help(message):
    await message.answer('Im bot and I can show your timetable on every day and every week or today. Also, I can give link for official site of mtuci, you '
                         'should write /mtuci and I can tell which week now, for this write /week')

# Бот не знает такой команды
@dp.message_handler()
async def any_message_answer(message):
    await message.answer('Sorry, but Im not understand, try /help for get list of commands')

if __name__ == '__main__':
    executor.start_polling(dp)
