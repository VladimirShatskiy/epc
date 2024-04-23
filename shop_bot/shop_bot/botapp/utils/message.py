from botapp.utils.decorators import timeit
from loader import bot
from telebot.apihelper import ApiTelegramException

from manage import logger
from shop_bot.settings import MY_DEBUG
from shopapp.models import MessagesId, Messages


@timeit
@logger.catch()
def message_add_to_sql(message, item: str = 'text', url: str = "") -> None:
    """
    Создание записи в модели Messages

    send_from: модель User отправителя сообщения
    send_to: модель User получателя сообщения
    send_text: Текс сообщений
    """

    if MY_DEBUG:
        logger.info("вход message_add_to_sql(message, item='text')")

    MessagesId.objects.create(
        telegram_id=message.chat.id,
        messages_id=message.id,
        item=item,
        url=url
        )

    if MY_DEBUG:
        logger.info("выход message_add_to_sql(message, item='text')")


@timeit
@logger.catch()
def message_delete(user_id: int, item='text') -> None:
    """
    Удаление всех сообщений из телеграм по пользователю
    :param item: Закладка для удаления, по умолчанию None
    :param user_id: id пользователя
    :return:
    """

    if MY_DEBUG:
        logger.info(f"вход message_delete(user_id: int, item=None {user_id}")

    messages = MessagesId.objects.filter(telegram_id=user_id, item=item)

    for message in messages:
        try:
            bot.delete_message(chat_id=user_id, message_id=message.messages_id)
        except ApiTelegramException:
            pass
        MessagesId.objects.filter(pk=message.pk).delete()

    if MY_DEBUG:
        logger.info(f"выход message_delete(user_id: int, item=None {user_id}")


@timeit
@logger.catch()
def message_to_sql(send_from: object, send_to: object, send_text: str) -> None:
    """
    Создание записи в модели Messages

    send_from: модель User отправителя сообщения
    send_to: модель User получателя сообщения
    send_text: Текс сообщений
    """

    if MY_DEBUG:
        logger.info("вход message_to_sql(send_from: object, send_to: object, send_text: str):")

    Messages.objects.create(message_from=send_from, message_to=send_to, message_text=send_text)

    if MY_DEBUG:
        logger.info("выход message_to_sql(send_from: object, send_to: object, send_text: str):")