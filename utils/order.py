from telebot.types import Message, ReplyKeyboardRemove
import os

import utils
from config_data.config import GlobalOrderDict
from keyboards import inline
from config_data.config import BRANCH_PHOTO
from keyboards.reply import yes_no
from loader import bot
import datetime
from loguru import logger


@logger.catch
def confirmation_sending_server(message: Message) -> bool:
    """
    Вызывает меню подтверждения отправки фото по ранее выбранному заказ наряду

    :return: bool
    """

    if not utils.check_ready_record.check(message):
        return False

    text = f'Загрузить фото на сервер по заказ наряду ?'
    # bot.delete_message(message.chat.id, id.message_id)
    id = bot.send_message(message.chat.id, text, reply_markup=yes_no.keyboard())

    @bot.message_handler(content_types=['text'])
    # забираем ответ на запрос
    def message_input_step(message: Message):
        if message.text.lower() == "да":
            bot.send_message(message.chat.id, f'ok!', reply_markup=ReplyKeyboardRemove())
            return True
        else:
            bot.send_message(message.chat.id, 'Данные сохранены на устройстве, их можно будет загрузить позже'
                             , reply_markup=ReplyKeyboardRemove())
            choice(message)
            return False
    bot.register_next_step_handler(message, message_input_step)
    return False


@logger.catch
def choice(message: Message):

    global GlobalOrderDict
    dict.clear(GlobalOrderDict)
    try:
        for item in os.listdir(BRANCH_PHOTO):
            if os.path.isdir(os.path.join(BRANCH_PHOTO, item)):
                str_date = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(BRANCH_PHOTO, item)))
                shot_date = str_date.strftime("%d %m %Y")
                if shot_date in GlobalOrderDict:
                    if item not in GlobalOrderDict[shot_date]:
                        GlobalOrderDict[shot_date] += [item]
                else:
                    GlobalOrderDict[shot_date] = [item]
        bot.send_message(message.chat.id, "Просьба выбрать день для выбора заказ наряда",
                         reply_markup=inline.calendar.keyboard(GlobalOrderDict.keys()))

    except FileNotFoundError:
        bot.send_message(message.chat.id, 'Отсутствует путь к папке с заказ нарядами')
