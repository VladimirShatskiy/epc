import json
import os
from utils import search_number
from loader import bot
from config_data.config import GlobalOrderDict, BRANCH_USER_DATA, CUR, CONNECT_BASE
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
            bot.send_message(call.from_user.id, 'Произошла ошибка памяти,\n'
                                                ' просьба начать заново выбрав в меню команду\n/order')

    if call.data.split(',')[0] == "order":
        data = (call.data.split(',')[1], call.from_user.id,)
        CUR.execute("""UPDATE users SET "order" = ? WHERE telegram_id = ?""", data)
        CONNECT_BASE.commit()
        up_message.up_message(call.from_user.id)
        type_order.bot_type(call)

    if call.data == "search_number":
        search_number.get_number(call.from_user.id)

    if call.data.split(',')[0] == "type":
        data = (call.data.split(',')[1],call.data.split(',')[2], call.from_user.id,)
        CUR.execute("""UPDATE users SET "order_type_rus" = ?, "order_type" = ? WHERE telegram_id = ?""", data)
        CONNECT_BASE.commit()

        up_message.up_message(call.from_user.id)



