from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура администратора

    :param type_dict: загруженный список действий

    :return: keyboard
    """
    markup = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton("Смена уровня доступа", callback_data='change_level_access')
    markup.add(button1)
    button2 = InlineKeyboardButton("Смена имени пользователя", callback_data='change_name_user')
    markup.add(button2)
    button3 = InlineKeyboardButton("Просмотр протокола беседы", callback_data='view_dialog')
    markup.add(button3)
    button4 = InlineKeyboardButton("Просмотр протокола бесед вне заказ нарядов", callback_data='view_all_dialog')
    markup.add(button4)
    button5 = InlineKeyboardButton("Смена 'активности' пользователя ", callback_data='change_active')
    markup.add(button5)

    return markup