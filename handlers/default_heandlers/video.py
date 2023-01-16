import json

from telebot.types import Message
from loader import bot
import requests
from config_data.config import BOT_TOKEN, BRANCH_PHOTO, BRANCH_USER_DATA
import os
from loguru import logger


@bot.message_handler(content_types=['video'])
@logger.catch
def bot_video(message: Message):

    file_date = str(message.from_user.id) + '_conf.txt'
    file_string = os.path.join(BRANCH_USER_DATA, file_date)
    with open(file_string, 'r', encoding='utf-8') as file:
        data = json.load(file)

    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

    way = os.path.join(BRANCH_PHOTO, data['order'], data['type'], file_id + '.mov')

    try:
        with open(way, 'wb') as open_file:
            open_file.write(file.content)
    except FileNotFoundError:
        os.mkdir(os.path.join(BRANCH_PHOTO, data['order'], data['type']))
        with open(way, 'wb') as open_file:
            open_file.write(file.content)
