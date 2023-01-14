from telebot.types import Message
from loader import bot
import requests
from config_data.config import BOT_TOKEN
import os


@bot.message_handler(content_types=['photo'])
def bot_photo(message: Message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))
    way = os.path.join('photo/' + file_id + '.png')
    with open(way, 'wb') as open_file:
        open_file.write(file.content)
