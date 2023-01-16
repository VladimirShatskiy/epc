from telebot.types import Message, ReplyKeyboardRemove
import os
from config_data.config import GlobalOrderDict
from keyboards import inline
from config_data.config import BRANCH_PHOTO
from keyboards.reply import yes_no
from loader import bot
import datetime


def confirmation_sending_server(message: Message):
    """
    Вызывает меню подтверждения отправки фото по ранее выбранному заказ наряду

    :return:
    """

    text = f'Загрузить фото на сервер по заказ наряду ?'
    bot.send_message(message.chat.id, text, reply_markup=yes_no.keyboard())

    @bot.message_handler(content_types=['text'])
    # забираем ответ на запрос
    def message_input_step(message: Message):
        if message.text.lower() == "да":
            bot.send_message(message.chat.id, f'ok!', reply_markup=ReplyKeyboardRemove())
            return
        else:
            bot.send_message(message.chat.id, 'Загружаю список заказ нарядов', reply_markup=ReplyKeyboardRemove())
            choice(message)
            return
    bot.register_next_step_handler(message, message_input_step)


def choice(message: Message):

    global GlobalOrderDict
    for item in os.listdir(BRANCH_PHOTO):
        if os.path.isdir(os.path.join(BRANCH_PHOTO, item)):
            str_date = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(BRANCH_PHOTO, item)))
            shot_date = str_date.strftime("%d %m %Y")
            if shot_date in GlobalOrderDict:
                GlobalOrderDict[shot_date] += [item]
            else:
                GlobalOrderDict[shot_date] = [item]

    bot.send_message(message.chat.id, "Просьба выбрать день для выбора заказ наряда",
                     reply_markup=inline.calendar.keyboard(GlobalOrderDict.keys()))

