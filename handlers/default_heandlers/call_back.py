from telebot.types import Message
from utils import search_number
from handlers.default_heandlers import start
from loader import bot
from config_data.config import GlobalOrderDict, GlobalOrder
from keyboards import inline
from loguru import logger


@logger.catch
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Сборщик ответов всех кнопок
    :param call:
    :return:
    """
    global GlobalOrderDict
    if call.data.split(',')[0] == "calendar":

        try:
            bot.send_message(call.from_user.id, "Просьба выбрать заказ наряд",
                             reply_markup=inline.choice_order.keyboard(GlobalOrderDict[call.data.split(',')[1]]))
        except:
            bot.send_message(call.from_user.id, 'Произошла ошибка памяти,\n'
                                                ' просьба начать заново выбрав в меню команду\n/order')

    if call.data.split(',')[0] == "order":
        try:
            GlobalOrder = call.data.split(',')[1]
            text = f"Выбран заказ наряд {GlobalOrder}\n можно загружать по нему фото"
            bot.send_message(call.from_user.id, text)

        except:
            bot.send_message(call.from_user.id, 'Произошла ошибка памяти,\n'
                                                ' просьба начать заново выбрав в меню команду\n/order')

    if call.data == "search_number":
        search_number.get_number(call.from_user.id)






