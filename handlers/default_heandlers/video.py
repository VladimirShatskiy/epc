
from telebot.types import Message
from loader import bot
import requests
from config_data.config import BOT_TOKEN, BRANCH_PHOTO, CUR, lock
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

    data_sql = (data[0],)
    lock.acquire(True)
    CUR.execute("""SELECT telegram_id, order_type_rus FROM users WHERE "order" = ? and user_type = 3""", data_sql)
    data_for_send_id = CUR.fetchone()
    data_sql = (message.from_user.id,)
    CUR.execute("""SELECT order_type_rus FROM users WHERE "telegram_id" = ? """, data_sql)
    data_for_send_type = CUR.fetchone()
    lock.release()
    try:

        bot.send_video(data_for_send_id[0], file.content, data_for_send_type[0])
        error_mes = False
    except TypeError:
        error_mes = True

    if message.media_group_id:
        if message.media_group_id == ID:
            pass
        else:
            ID = message.media_group_id
            bot.send_message(message.from_user.id, "Загрузил видео из альбома на сервер")
            if error_mes:
                bot.send_message(message.from_user.id, "!!! Видео из альбома НЕ отправлено клиенту !!!")
            else:
                bot.send_message(message.from_user.id, "Видео из альбома отправлено клиенту")
    else:
        bot.send_message(message.from_user.id, "Загрузил видео на сервер")
        if error_mes:
            bot.send_message(message.from_user.id, "!!! Видео НЕ отправлено клиенту !!!")
        else:
            bot.send_message(message.from_user.id, "Видео отправлено клиенту")
