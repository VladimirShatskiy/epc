import json
import os
from loader import bot
from telebot.types import Message
from config_data.config import BRANCH_USER_DATA


def check(message: Message) -> bool:
    """
    Проверка на готовность пути размещения фотографий
    :param message: Message
    :return: bool
    """
    file_date = str(message.from_user.id) + '_conf.txt'
    file_string = os.path.join(BRANCH_USER_DATA, file_date)
    with open(file_string, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if data['order'] == '' or data['type'] == '':
        bot.send_message(message.from_user.id, 'Не выбран заказ наряд или тип действия, '
                                  'просьба повторить выбор перед отправкой фотографий')
        return False
    else:
        return True
