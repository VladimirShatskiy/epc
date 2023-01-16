from telebot.types import Message
from loader import bot
import requests
from config_data.config import BOT_TOKEN, BRANCH_PHOTO
import os
from utils.order import confirmation_sending_server


@bot.message_handler(content_types=['photo'])
def bot_photo(message: Message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

    # подтверждение ввода по заказ наряду

    confirmation_sending_server(message)

    way = os.path.join(BRANCH_PHOTO, file_id + '.png')

    with open(way, 'wb') as open_file:
        open_file.write(file.content)
