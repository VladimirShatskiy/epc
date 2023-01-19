from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard(order_list: list) -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора списка заказ нарядов
    :param order_list: заказ наряд
    :return: keyboard
    """

    markup = InlineKeyboardMarkup()
    for item in order_list:
        button = InlineKeyboardButton(item, callback_data='order,' + item)
        markup.row(button)

    return markup
