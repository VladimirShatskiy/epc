from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard(id) -> InlineKeyboardMarkup:
    """
    Клавиатура администратора

    :param type_dict: кнопка возврата к заказ наряду

    :return: keyboard
    """
    markup = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton(f"Ответить клиенту", callback_data='reply_to_client,'+str(id))
    markup.add(button1)
    return markup