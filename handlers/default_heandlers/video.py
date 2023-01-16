from telebot.types import Message
from loader import bot
import requests
from config_data.config import BOT_TOKEN, BRANCH_PHOTO
import os
from loguru import logger


@bot.message_handler(content_types=['video'])
@logger.catch
def bot_video(message: Message):
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))
    way = os.path.join(BRANCH_PHOTO, file_id + '.mov')
    with open(way, 'wb') as open_file:
        open_file.write(file.content)