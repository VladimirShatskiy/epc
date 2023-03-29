import json
import os
import handlers.default_heandlers.admin
from utils import search_number, barcode
from loader import bot
from config_data.config import GlobalOrderDict, CUR, CONNECT_BASE, BRANCH_PHOTO, lock
from keyboards import inline
from loguru import logger
from handlers.default_heandlers import up_message, type_order
from utils.get_plate_number import get_plate_number_start


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
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                                  text="Просьба выбрать заказ наряд",
                                  reply_markup=inline.choice_order.keyboard(GlobalOrderDict[call.data.split(',')[1]]))
        except:
            bot.send_message(call.from_user.id, 'Произошла ошибка,\n'
                                                ' просьба начать заново выбрав в меню команду\n/order')
    elif call.data == 'get_barcode':
        barcode.barcode_start(call)

    elif call.data == 'get_plate_number':
        get_plate_number_start(call)

    elif call.data.split(',')[0] == "order":
        data = (call.data.split(',')[1], call.from_user.id,)
        with lock:
            CUR.execute("""UPDATE users SET "order" = ? WHERE telegram_id = ?""", data)
            CONNECT_BASE.commit()

        up_message.up_message(call.from_user.id)

#  Проверка наличия телефонного номера в папке заказ наряда
        try:
            way = os.path.join(BRANCH_PHOTO, data[0], 'content.txt')
            with open(way, 'r') as open_file:
                data = json.load(open_file)
                phone = data['phone']

            data_sql = (data['order'], phone)
            with lock:
                CUR.execute("""UPDATE users SET "order" = ? WHERE  "phone" = ?""", data_sql)
                CONNECT_BASE.commit()

        except FileNotFoundError:
            bot.send_message(call.from_user.id, "!!!ВНИМАНИЕ!!!\n"
                                                "Не подгружен телефон клиента\n"
                                                "Отправка фото клиенту невозможна")
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                              text="Обновил информацию в закрепленной троке", reply_markup="")
        type_order.bot_type(call)

    elif call.data == "search_number":
        search_number.get_number(call.from_user.id)

    elif call.data.split(',')[0] == "type":
        data = (call.data.split(',')[1], call.data.split(',')[2], call.from_user.id,)
        with lock:
            CUR.execute("""UPDATE users SET "order_type_rus" = ?, "order_type" = ? WHERE telegram_id = ?""", data)
            CONNECT_BASE.commit()
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id,
                              text="Обновил информацию в закрепленной строке", reply_markup="")
        up_message.up_message(call.from_user.id)

    elif call.data == "change_level_access":
        handlers.default_heandlers.admin.change_level_access(call)

    elif call.data == "change_name_user":
        handlers.default_heandlers.admin.change_name(call)

    elif call.data == "view_dialog":
        handlers.default_heandlers.admin.view_dialog(call)

    elif call.data == "change_active":
        handlers.default_heandlers.admin.change_active(call)

    elif call.data.split(',')[0] == "reply_to_client":
        handlers.default_heandlers.reply_to_client.reply(call, id_client=call.data.split(',')[1])

    elif call.data == "view_all_dialog":
        handlers.default_heandlers.admin.view_all_dialog(call)




