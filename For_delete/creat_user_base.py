from telebot.types import Message
from handlers.custom_handlers import survey


def create_user_base(message: Message) -> None:
    """
    Создание строки в базе с данными клиента
    """
    survey.survey(message)



