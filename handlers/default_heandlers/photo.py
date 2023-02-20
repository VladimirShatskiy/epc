from telebot.types import Message
from loader import bot
import requests
from config_data.config import BOT_TOKEN, BRANCH_PHOTO, CUR, lock, CONNECT_BASE
import os
from loguru import logger
ID = 1


@bot.message_handler(content_types=['photo'])
@logger.catch
def bot_photo(message: Message):

    global ID

    data = (message.from_user.id,)
    with lock:
        CUR.execute("""SELECT "order", "order_type" FROM users WHERE "telegram_id" = ? """, data)
    data = CUR.fetchone()

    if data[0] == "" or data[1] == "":
        bot.send_message(message.from_user.id, "Ошибка!!! \nНевозможно загрузить фото\n"
                                               "Для загрузки необходимо выбрать \n"
                                               "заказ наряд /order \n"
                                               "и тип действия /type\n\n"
                                               "Обратите внимание на верхнее закрепленное сообщение, "
                                               "в нем указывается заказ наряд и тип действия")
        return

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

    way = os.path.join(BRANCH_PHOTO, data[0], data[1], file_id + '.png')
    if not os.path.isdir(os.path.join(BRANCH_PHOTO, data[0], data[1])):
        os.mkdir(os.path.join(BRANCH_PHOTO, data[0], data[1]))
    with open(way, 'wb') as open_file:
        open_file.write(file.content)

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
            data = (data_sql[0], data_for_send_id[0])
            with lock:
                CUR.execute("""UPDATE users SET to_answer_id = ? WHERE telegram_id = ?""", data)
                CONNECT_BASE.commit()
            bot.send_photo(data_for_send_id[0], file.content, data_for_send_type[0])
            error_mes = False
    except TypeError:
        error_mes = True

    if message.media_group_id:
        if message.media_group_id == ID:
            pass
        else:
            ID = message.media_group_id
            bot.send_message(message.from_user.id, "Загрузил фото из альбома на сервер")
            if error_mes:
                bot.send_message(message.from_user.id, "!!! Альбом фотографий НЕ отправлен клиенту !!!")
            else:
                bot.send_message(message.from_user.id, "Альбом фотографий отправлен клиенту")
    else:
        bot.send_message(message.from_user.id, "Загрузил фото на сервер")
        if error_mes:
            bot.send_message(message.from_user.id, "!!! Фотография НЕ отправлена клиенту !!!")
        else:
            bot.send_message(message.from_user.id, "Фотография отправлена клиенту")
