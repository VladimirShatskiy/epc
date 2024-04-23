from loader import bot
from telebot.types import Message

from shopapp.models import OrderProduct


def pin_message(order: object, message: Message) -> None:
    """
    Закрепление сообщения
    :param order:  заказ
    :param message:
    :return: None (Изменяет закрепленную строку)
    """

    products = OrderProduct.objects.filter(order=order)

    count, total = 0, 0

    for product in products:
        count += product.count
        total += product.count * product.price

    to_pin = bot.send_message(message.from_user.id, f'В корзине {count} товаров на Сумму {total} рублей').message_id
    bot.pin_chat_message(chat_id=message.from_user.id, message_id=to_pin, disable_notification=True)
    bot.delete_message(message.chat.id, message.message_id)
