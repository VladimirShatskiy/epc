from telebot.types import ReplyKeyboardMarkup


def keyboard() -> ReplyKeyboardMarkup:
    """
    Простая клавиатура Да/Нет
    :return: keyboard
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Да")
    markup.add("Нет")
    return markup
