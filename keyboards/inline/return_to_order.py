from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard(order) -> InlineKeyboardMarkup:
    """
    Клавиатура администратора

    :param type_dict: кнопка возврата к заказ наряду

    :return: keyboard
    """
    markup = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton(f"Переключиться на заказ наряд {order}", callback_data='order,'+str(order))
    markup.add(button1)
    return markup