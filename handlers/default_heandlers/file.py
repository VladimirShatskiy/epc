from telebot.types import Message
from config_data.config import BRANCH_PHOTO
from loader import bot
import os


@bot.message_handler(content_types=['document'])
def bot_file(message: Message):

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    way = os.path.join(BRANCH_PHOTO, message.document.file_name)
    with open(way, 'wb') as open_file:
        open_file.write(downloaded_file)
