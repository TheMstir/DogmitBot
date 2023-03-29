import chunk

import request
import random
import telebot
import time
import datetime
import config
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot import types


# @DogmeetRestbot
cash_storage = StateMemoryStorage()


# тут ключик и база данных от самого телеграмма
bot = telebot.TeleBot(config.telegram_key, state_storage=cash_storage)





class MyStates(StatesGroup):
    """Хранлилище для промежуточных данных """
    username = State()







@bot.message_handler(regexp='Привет', 'Вабалабадабдаб', 'Гав')
@bot.message_handler(commands=['hello-world'])
def hello_start(message: types.Message):
    """
    Бот здоровается несколькими вариантами в ответ на преветсвие
    """
    dice = random.randint(0, 4)
    mes = ''
    if dice == 0:
        mes = 'Готов к работе!🐺'
    elif dice == 1:
        mes = 'Привет! Я маленький рыжий пес!\nВернее я цифровой бот-пес\nВкусняшки мне не нужны😋'
    elif dice == 2:
        mes = 'Привет! 👋 У нас принято начинать с команды /start 🍗'
    elif dice == 3:
        mes = 'Это лишь тестовая версия, я обязательно всему научусь и помогу вам, но позже🐕🥫'
    elif dice == 4:
        mes = nero_humor()

    bot.send_message(message.chat.id, mes, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    rand_m = random.randint(1, 2)
    if rand_m == 1:
        mess = f'Bau-Wau <b>{message.from_user.first_name}</b> я бот-Песмит!\n' \
               f'с (◕ᴥ◕ʋ)"!\n' \
               f' '
    else:
        mess = f'Привет! <b>{message.from_user.first_name}</b> я собачка 🐕 Песмит!, из веб-комикса Dogmit' \
               f'Я здесь для того чтобы дать тебе посмотреть случайный выпуск, послушать шутки, факты, или' \
               f'немного со мной поиграть!'
    bot.send_message(message.chat.id, mess, parse_mode='HTML')
    time.sleep(1)
    bot.send_message(message.chat.id, f'Смотри на меню что появилось над клавиатурой и не запутаешься\n'
                                      f'Но если что хочешь узнать то жми /help,\n'
                                      f'Гав-Гав! Все знаешь - давай приступать\n')
    if rand_m == 1:
    time.sleep(1)

    humor = nero_humor()
    bot.send_message(message.chat.id, humor)


@bot.message_handler(commands=['fast_menu'])
# сам хендлер для теста потом будет интегрировано в тело старта.
def menu(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👋 Случайный", "❓ Help/Menu")
    bot.send_message(message.from_user.id, 'ok', reply_markup=markup)


@bot.message_handler(commands=['help'])
def show_help_menu(message: types.Message):
    """
    Меню навигации в виде записи для помощи
    позволяет быстро перейти к основному функционалу
    иногда подкидывает факт из списка
    """
    mess = '''Гав! 🐶 Вот что мы можем сделать прямо сейчас:
/start чтобы начать наше общение
💼💰
/weather чтобы ознакомиться с погодой🌅
/history отправляет вам вашу историю запросов
/cancel ❌ отменяет введенные данные и позволяет ввести новый запрос города ♻️
Можем просто немного пообщаться, но помни что я всего-лишь цифровой 🐕‍🦺 бот-песик и умею не так уж и много
    '''
    bot.send_message(message.chat.id, mess, parse_mode='HTML')
    dice = random.randint(1, 6)
    if dice == 6:
        time.sleep(0.5)
        bot.send_message(message.chat.id, facts())


@bot.message_handler(commands=['homeland_rus'])
def homelandrus(message: types.Message):
    """Функция поиска отелей в регионе
    где нет gaiaId, соответственно без сортировки, просто выдачей
    """
    bot.send_message(message.chat.id, 'Поищем местные отели:  ️🈂️')
    time.sleep(1)
    sent = bot.send_message(message.chat.id, 'В каком городе будем искать?: ')
    bot.register_next_step_handler(sent, homeland)


@bot.message_handler(commands=['low_price'])
def low_price(message: types.Message):
    """Функция поиска отелей с самой низкой ценой
    выставляет флаг поиска по 'PRICE_LOW_TO_HIGH'
    ведет к цепочке стандартного сбора информации
    """
    bot.send_message(message.chat.id, 'Поищем дешевые отели:  ️🈂️')
    bot.set_state(message.from_user.id, MyStates.flag, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['flag'] = 'PRICE_LOW_TO_HIGH'
    time.sleep(1)
    bot.send_message(message.chat.id, 'В каком городе будем искать?: ')

    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)


@bot.message_handler(commands=['high_price'])
def high_price(message: types.Message):
    """
    """
    bot.send_message(message.chat.id, 'Будем искать лучшие предложения: 💸️🧐')

    bot.set_state(message.from_user.id, MyStates.flag, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['flag'] = 'T' # так он забивает данные на позицию

    time.sleep(0.2)
    bot.send_message(message.chat.id, 'Буду стараться🐕! В каком городе ищем?: ')

    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)




def nero_humor():
    """
    Take a 1 'humor' line from ChatGPT humor about DOG and return to user
    Можно дополнять шутками, база на данный момент просто txt фаил
    """
    with open('dogmitGPTHumor.txt', 'r', encoding='utf-8') as file:
        lf = file.read().count('\n')
        dice = random.randint(1, lf)
        mess = file.read().split('\n')
        humor = mess[dice]
    return humor