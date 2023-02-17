import json

from telebot.types import Message
from loader import bot
import requests
from config_data.config import BOT_TOKEN, BRANCH_PHOTO, BRANCH_USER_DATA, CUR, lock
import os
from loguru import logger
ID = 1


@bot.message_handler(content_types=['video'])
@logger.catch
def bot_video(message: Message):

    global ID

    lock.acquire(True)
    data = (message.from_user.id,)
    CUR.execute("""SELECT "order", "order_type" FROM users WHERE "telegram_id" = ? """, data)
    data = CUR.fetchone()
    lock.release()

    if data[0] == "" or data[1] == "":
        bot.send_message(message.from_user.id, "Ошибка!!! \nНевозможно загрузить видео\n"
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
            bot.send_message(message.from_user.id, "Загрузил видео из альбома на сервер")
    else:
        bot.send_message(message.from_user.id, "Загрузил видео на сервер")



    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

    way = os.path.join(BRANCH_PHOTO, data[0], data[1], file_id + '.mov')
    if os.path.isdir(os.path.join(BRANCH_PHOTO, data[0], data[1])):
        with open(way, 'wb') as open_file:
            open_file.write(file.content)
    else:
        os.mkdir(os.path.join(BRANCH_PHOTO, data[0], data[1]))
        with open(way, 'wb') as open_file:
            open_file.write(file.content)
