from telebot.types import Message
from loader import bot
import requests
from config_data.config import BOT_TOKEN
import os


@bot.message_handler(content_types=['document'])
def bot_file(message: Message):

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    way = os.path.join('photo/' + message.document.file_name)
    with open(way, 'wb') as open_file:
        open_file.write(downloaded_file)
