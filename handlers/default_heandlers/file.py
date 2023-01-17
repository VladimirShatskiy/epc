import json

from telebot.types import Message
from config_data.config import BRANCH_PHOTO, BRANCH_USER_DATA
from loader import bot
import os
from loguru import logger


@bot.message_handler(content_types=['document'])
@logger.catch
def bot_file(message: Message):

    file_date = str(message.from_user.id) + '_conf.txt'
    file_string = os.path.join(BRANCH_USER_DATA, file_date)
    with open(file_string, 'r', encoding='utf-8') as file:
        data = json.load(file)

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    way = os.path.join(BRANCH_PHOTO, data['order'], data['type'], message.document.file_name)
    if os.path.isdir(os.path.join(BRANCH_PHOTO, data['order'], data['type'])):
        with open(way, 'wb') as open_file:
            open_file.write(downloaded_file)
    else:
        os.mkdir(os.path.join(BRANCH_PHOTO, data['order'], data['type']))
        with open(way, 'wb') as open_file:
            open_file.write(downloaded_file)

