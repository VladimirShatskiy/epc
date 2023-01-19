import json
from telebot.types import Message
from loader import bot
import requests
from config_data.config import BOT_TOKEN, BRANCH_PHOTO, BRANCH_USER_DATA
import os
from loguru import logger
ID = 1


@bot.message_handler(content_types=['photo'])
@logger.catch
def bot_photo(message: Message):

    global ID

    file_date = str(message.from_user.id) + '_conf.txt'
    file_string = os.path.join(BRANCH_USER_DATA, file_date)
    with open(file_string, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data['order'] == "" or data['type'] == "":
        bot.send_message(message.from_user.id, "Ошибка!!! \nНевозможно загрузить фото\n"
                                               "Для загрузки необходимо выбрать \n"
                                               "заказ наряд /order \n"
                                               "и тип действия /type\n\n"
                                               "Обратите внимание на верхнее закрепленное сообщение, "
                                               "в нем указывается заказ наряд и тип действия")
        return

    if message.media_group_id:
        if message.media_group_id == ID:
            pass
        else:
            ID = message.media_group_id
            bot.send_message(message.from_user.id, "Загрузил фото из альбома на сервер")
    else:
        bot.send_message(message.from_user.id, "Загрузил фото на сервер")

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

    way = os.path.join(BRANCH_PHOTO, data['order'], data['type'], file_id + '.png')
    if os.path.isdir(os.path.join(BRANCH_PHOTO, data['order'], data['type'])):
        with open(way, 'wb') as open_file:
            open_file.write(file.content)
    else:
        os.mkdir(os.path.join(BRANCH_PHOTO, data['order'], data['type']))
        with open(way, 'wb') as open_file:
            open_file.write(file.content)
