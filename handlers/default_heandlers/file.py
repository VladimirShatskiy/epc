from telebot.types import Message
from config_data.config import BRANCH_PHOTO, CUR, lock
from loader import bot
import os
from loguru import logger
ID = 1


@bot.message_handler(content_types=['document'])
@logger.catch
def bot_file(message: Message):

    global ID
    data = (message.from_user.id,)
    with lock:
        CUR.execute("""SELECT "order", "order_type" FROM users WHERE "telegram_id" = ? """, data)
    data = CUR.fetchone()


    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    way = os.path.join(BRANCH_PHOTO, data[0], data[1], message.document.file_name)
    if os.path.isdir(os.path.join(BRANCH_PHOTO, data[0], data[1])):
        with open(way, 'wb') as open_file:
            open_file.write(downloaded_file)
    else:
        os.mkdir(os.path.join(BRANCH_PHOTO, data[0], data[1]))
        with open(way, 'wb') as open_file:
            open_file.write(downloaded_file)

    data_sql = (data[0],)
    with lock:
        CUR.execute("""SELECT telegram_id, order_type_rus FROM users WHERE "order" = ? and user_type = 3""", data_sql)
    data_for_send_id = CUR.fetchone()
    data_sql = (message.from_user.id,)
    with lock:
        CUR.execute("""SELECT order_type_rus, order_type FROM users WHERE "telegram_id" = ? """, data_sql)
    data_for_send_type = CUR.fetchone()

    try:
        if data_for_send_type[1] == "Service":
            error_mes = True
        else:
            bot.send_document(data_for_send_id[0], downloaded_file, data_for_send_type[0])
            error_mes = False
    except TypeError:
        error_mes = True

    if message.media_group_id:
        if message.media_group_id == ID:
            pass
        else:
            ID = message.media_group_id
            bot.send_message(message.from_user.id, "Загрузил файл из альбома на сервер")
            if error_mes:
                bot.send_message(message.from_user.id, "!!! Файлы из альбома НЕ отправлены клиенту !!!")
            else:
                bot.send_message(message.from_user.id, "Файлы из альбома отправлены клиенту")
    else:
        bot.send_message(message.from_user.id, "Загрузил файл на сервер")
        if error_mes:
            bot.send_message(message.from_user.id, "!!! Файл НЕ отправлен клиенту !!!")
        else:
            bot.send_message(message.from_user.id, "Файл отправлен клиенту")
