from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from botapp.utils.decorators import timeit
from manage import logger


@timeit
@logger.catch
def all_orders(orders: list[object]) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры со списком всех заказов пользователя
    """

    markup = InlineKeyboardMarkup()

    for order in orders:
        button = InlineKeyboardButton(f'Заказ {order.pk} создан {order.create_at} статус {order.status}',
                                      callback_data='get_order_by_number,' + str(order.pk))
        markup.row(button)

    return markup

