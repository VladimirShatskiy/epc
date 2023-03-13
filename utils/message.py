import os
from datetime import datetime
from loguru import logger

from config_data.config import BRANCH_PHOTO, CUR, lock
from loader import bot


@logger.catch()
def record_message(id_user, order, message_text, user_type):
    """
    Протокол записи беседы по заказ наряду
    :param id_user: id Telegram
    :param order: номер заказ наряда
    :param message_text: текс отправленного сообщения
    :return:
    """

    file_date = 'recording_dialog_' + str(order) + '.txt'
    file_string = os.path.join(BRANCH_PHOTO, str(order), file_date)
    text = datetime.now().ctime() + \
        '\nЗаказ наряд/id ' + str(order) + ' Пользователь ' + str(id_user) + ' ' + str(user_type) + \
        '\nСообщение: ' + message_text + '\n\n'

    try:
        with open(file_string, 'a', encoding='utf-8') as file:
            file.write(text)
    except FileNotFoundError:
        # Сообщение поступает всем админам о сообщении от клиента при закрытом заказ наряде
        file_date = 'all_recording_dialog.txt'
        file_string = os.path.join(BRANCH_PHOTO, file_date)

        with open(file_string, 'a', encoding='utf-8') as file:
            file.write(text)

        with lock:
            CUR.execute("""SELECT telegram_id FROM users WHERE user_type = 1""")
        admins = CUR.fetchall()
        text = "<b><i>Обратите внимание!</i></b> ведется переписка при закрытом заказ наряде\n" \
               "история записана в общий файл переписки\n" \
               f"Закрытый заказ наряд/id клиента {str(order)}\n" \
               f"Сообщение\n" \
               f"{message_text}"
        for admin in admins:
            bot.send_message(admin[0], text, parse_mode='html')