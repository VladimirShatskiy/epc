from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_contact() -> ReplyKeyboardMarkup:
    """
    Кнопка для опроса, подтверждение передачи номера телефона
    """
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton("Отправить номер телефона", request_contact=True))
    return keyboard
