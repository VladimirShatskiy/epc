from telebot.types import Message
from config_data.config import GlobalOrderDict
from loader import bot
from keyboards import inline
from loguru import logger


def get_number(message: Message):
    mesg = bot.send_message(message, 'Просьба ввести заказ наряд для поиска')
    bot.register_next_step_handler(mesg, search)


@logger.catch
def search(message: Message):
    order_list = []
    if GlobalOrderDict == {}:
        bot.send_message(message.chat.id, 'Ошибка памяти\n Просьба повторить поиск заказ нарядов /order')
    else:
        bot.send_message(message.chat.id, 'Спасибо, ищу')

    for item in GlobalOrderDict.keys():
        for i in GlobalOrderDict[item]:
            if message.text in i:
                order_list.append(i)

    if not order_list:
        bot.send_message(message.chat.id, "По входным данным заказ наряд не найден\n"
                                          "Обновите запрос или выберите дату для поиска",
                         reply_markup=inline.calendar.keyboard(GlobalOrderDict.keys()))
    else:
        bot.send_message(message.chat.id, "Просьба выбрать заказ наряд из списка",
                         reply_markup=inline.choice_order.keyboard(order_list))

