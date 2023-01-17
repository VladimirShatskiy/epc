import json
import os
from config_data.config import BRANCH_USER_DATA
from loader import bot


def up_message(message):

    bot.unpin_all_chat_messages(message)
    file_date = str(message) + '_conf.txt'
    file_string = os.path.join(BRANCH_USER_DATA, file_date)
    with open(file_string, 'r', encoding='utf-8') as file:
        data = json.load(file)

    text = f'ЗН {data["order"]} тип {data["rus_type"]}'

    to_pin = bot.send_message(message, text).message_id
    bot.pin_chat_message(chat_id=message, message_id=to_pin)