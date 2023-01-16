from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard(type_list: list) -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора типа фотографий к заказ наряду

    :param order_list: список заказ нарядов

    :return: keyboard
    """
    markup = InlineKeyboardMarkup()
    for item in sorted(type_list):
        button = InlineKeyboardButton(item, callback_data='type,' + item)
        markup.add(button)
    button = InlineKeyboardButton("Найти заказ наряд по номеру", callback_data='search_number')
    markup.add(button)
    return markup