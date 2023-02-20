import os

import handlers.default_heandlers.admin
from utils import search_number
from loader import bot
from config_data.config import GlobalOrderDict, CUR, CONNECT_BASE, BRANCH_PHOTO, lock
from keyboards import inline
from loguru import logger
from handlers.default_heandlers import up_message
from handlers.default_heandlers import type_order


@bot.callback_query_handler(func=lambda call: True)
@logger.catch
def callback_query(call):
    """
    Сборщик ответов всех кнопок
    :param call:
    :return:
    """

    if call.data.split(',')[0] == "calendar":
        try:
            bot.send_message(call.from_user.id, "Просьба выбрать заказ наряд",
                             reply_markup=inline.choice_order.keyboard(GlobalOrderDict[call.data.split(',')[1]]))
        except:
            bot.send_message(call.from_user.id, 'Произошла ошибка,\n'
                                                ' просьба начать заново выбрав в меню команду\n/order')

    elif call.data.split(',')[0] == "order":
        data = (call.data.split(',')[1], call.from_user.id,)
        with lock:
            CUR.execute("""UPDATE users SET "order" = ? WHERE telegram_id = ?""", data)
            CONNECT_BASE.commit()

        up_message.up_message(call.from_user.id)

#  Проверка наличия телефонного номера в папке заказ наряда
        try:
            way = os.path.join(BRANCH_PHOTO, data[0], 'phone.txt')
            with open(way, 'r') as open_file:
                phone = open_file.read()

            data_sql = (data[0], phone)
            with lock:
                CUR.execute("""UPDATE users SET "order" = ? WHERE  "phone" = ?""", data_sql)
                CONNECT_BASE.commit()

        except FileNotFoundError:
            bot.send_message(call.from_user.id, "!!!ВНИМАНИЕ!!!\n"
                                                "Не подгружен телефон клиента\n"
                                                "Отправка фото клиенту невозможна")

        type_order.bot_type(call)

    elif call.data == "search_number":
        search_number.get_number(call.from_user.id)

    elif call.data.split(',')[0] == "type":
        data = (call.data.split(',')[1], call.data.split(',')[2], call.from_user.id,)
        with lock:
            CUR.execute("""UPDATE users SET "order_type_rus" = ?, "order_type" = ? WHERE telegram_id = ?""", data)
            CONNECT_BASE.commit()

        up_message.up_message(call.from_user.id)

    elif call.data == "change_level_access":
        handlers.default_heandlers.admin.change_level_access(call)

    elif call.data == "change_name_user":
        handlers.default_heandlers.admin.change_name(call)

    elif call.data == "view_dialog":
        handlers.default_heandlers.admin.view_dialog(call)

    elif call.data.split(' ')[0] == "return_order":
        print('sdfsd')



