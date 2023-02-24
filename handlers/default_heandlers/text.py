import datetime
import os
from loguru import logger
import keyboards.inline.return_to_order
from config_data.config import CUR, lock, ORGANIZATION_NAME, CONNECT_BASE, BRANCH_USER_DATA, BRANCH_PHOTO
from database.attention_words import ATTENTION_WORDS
from loader import bot
from keyboards import inline


@logger.catch
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """
    Получение любой текстовой строки и ее обработка.
    Если текст написан клиентом, поиск по ключевым словам недовольства, с отправкой к администратору
    Текс от клиента так же отправляется написавшему сообщение
    Если текс написал сотрудник сервиса, оно отправляется по номеру заказ наряда к клиенту

    Определение кто пишет сообщение
    1,2 сотрудники сервиса (сообщение отправляется клиенту)
    3 клиент (сообщение отправляется написавшему сотруднику сервиса
    :param message:
    :return:
    """
    employee_id = (message.from_user.id,)
    with lock:
        CUR.execute("""SELECT "access_level" FROM users JOIN access_level al  
        ON type_id = user_type WHERE telegram_id = ?""", employee_id)

    user_type = CUR.fetchone()[0]
    if user_type == 'admin' or user_type == 'employee':
        #  Действие при написании сообщения сотрудником сервиса
        with lock:
            CUR.execute("""SELECT "order" FROM users WHERE telegram_id = ?""", employee_id)
        order_from_sql = CUR.fetchone()
        with lock:
            CUR.execute("""SELECT telegram_id FROM users WHERE "order"= ? and user_type = 3""", order_from_sql)
        temp = CUR.fetchone()

        if temp is None:
            bot.send_message(message.from_user.id, 'Клиент по данному заказ наряду не подключен к боту'
                                                   ', отправка сообщения невозможна')
            return
        telegram_id_client = temp[0]

        # Приписываем клиенту ID написавшего ему мастера
        data = (str(employee_id[0]), telegram_id_client,)
        with lock:
            CUR.execute("""UPDATE users SET to_answer_id = ? WHERE telegram_id = ?""", data)
            CONNECT_BASE.commit()

        with lock:
            CUR.execute("""SELECT "name" FROM users WHERE telegram_id = ?""", employee_id)
        employee_name = CUR.fetchone()[0]

        record_message(id_user=str(employee_id[0]), order=str(order_from_sql[0]), message_text=message.text)

        text = f"<b><i>Сообщение от {employee_name}, {ORGANIZATION_NAME}</i></b>\n" \
               f"{message.text}"
        bot.send_message(telegram_id_client, text, parse_mode='html')

    elif user_type == 'client':

        client_id = employee_id
        with lock:
            CUR.execute("""SELECT "to_answer_id", "order" FROM "users" WHERE telegram_id = ?""", client_id)

        return_date = CUR.fetchall()
        if return_date[0][0] == "" or return_date[0][0] is None:
            bot.send_message(message.from_user.id, "Информации по состоянию Вашего автомобиля пока нет,"
                                                   "как только тут появятся какие либо сообщения можно будет связаться"
                                                   "с мастером и задать ему вопросы")
        else:
            text = f"<b><i>Ответ клиента, по заказ наряду {return_date[0][1]}</i></b>\n" \
                   f"{message.text}"
            record_message(id_user=str(client_id[0]), order=return_date[0][1], message_text=message.text)
            bot.send_message(return_date[0][0], text, parse_mode='html',
                             reply_markup=keyboards.inline.return_to_order.keyboard(return_date[0][1]))

        # Проверка на нехорошие слова в ответе клиента
        for word in ATTENTION_WORDS:
            if word in message.text.lower():
                with lock:
                    CUR.execute("""SELECT telegram_id FROM users WHERE user_type = 1""")
                admins = CUR.fetchall()
                text = "<b><i>Обратите внимание! возможно клиент оставил плохой комментарий\n" \
                       f"заказ наряд {return_date[0][1]}\n" \
                       f"Сообщение от клиента</i></b>\n" \
                       f"{message.text}"
                for admin in admins:
                    bot.send_message(admin[0], text, parse_mode='html')


@logger.catch
def record_message(id_user, order, message_text):
    """
    Протокол записи беседы по заказ наряду
    :param id_user: id Telegram
    :param order: номер заказ наряда
    :param message_text: текс отправленного сообщения
    :return:
    """

    file_date = 'recording_dialog_' + str(order) + '.txt'
    file_string = os.path.join(BRANCH_PHOTO, str(order), file_date)
    try:
        with open(file_string, 'a', encoding='utf-8') as file:
            text = datetime.datetime.now().ctime() + '\nЗаказ наряд ' + str(order) + ' Пользователь ' + id_user + \
                   '\nСообщение "' + message_text + '"\n'
            file.write(text)
    except FileNotFoundError:
        # Сообщение поступает всем админам о сообщении от клиента при закрытом заказ наряде
        with lock:
            CUR.execute("""SELECT telegram_id FROM users WHERE user_type = 1""")
        admins = CUR.fetchall()
        text = "<b><i>Обратите внимание! клиент написал сотруднику при закрытом заказ наряде\n" \
               "история записи сообщения не ведется\n" \
               f"заказ наряд {str(order)}\n" \
               f"Сообщение от клиента</i></b>\n" \
               f"{message_text}"
        for admin in admins:
            bot.send_message(admin[0], text, parse_mode='html')


