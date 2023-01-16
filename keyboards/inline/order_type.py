from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard(type_dict: dict) -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора действия по заказ наряду

    :param type_dict: загруженный список действий

    :return: keyboard
    """
    markup = InlineKeyboardMarkup()
    for item in type_dict.keys():
        button = InlineKeyboardButton(item, callback_data='type,' + item + ',' + type_dict[item])
        markup.add(button)

    return markup