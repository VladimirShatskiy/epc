from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard(order_list: list) -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора дня календаря с заказ нарядами
    Для наглядности клавиатура выводит последние 7 дней

    :param order_list: список заказ нарядов

    :return: keyboard
    """
    markup = InlineKeyboardMarkup()
    for item in sorted(order_list)[:7]:
        button = InlineKeyboardButton(item, callback_data='calendar,' + item)
        markup.add(button)
    button = InlineKeyboardButton("Найти заказ наряд по номеру", callback_data='search_number')
    markup.add(button)
    return markup
