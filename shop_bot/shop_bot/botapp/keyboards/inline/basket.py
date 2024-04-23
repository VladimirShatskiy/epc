from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from botapp.utils.decorators import timeit
from manage import logger


@timeit
@logger.catch
def put_basket(message: Message, product_id: int) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры каталога
    """

    try:
        message_id = message.message.id
    except AttributeError:
        message_id = message.id

    markup = InlineKeyboardMarkup()

    button = InlineKeyboardButton("➕ Добавить в корзину", callback_data='put_basket,' + str(product_id) +
                                                                      ',' + str(message_id))
    button1 = InlineKeyboardButton("🛍 Перейти в корзину", callback_data='basket')

    markup.row(button, button1)

    return markup


@timeit
def plus_minus(order_id: int, product_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура добавить/удалить одну позицию товара или удалить целиком
    :param order_id:
    :param product_id:
    :return:
    """

    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(" ➕ ", callback_data='product +,' + str(order_id) + ',' + str(product_id))
    button1 = InlineKeyboardButton(" ➖ ", callback_data='product -,' + str(order_id) + ',' + str(product_id))
    button2 = InlineKeyboardButton("❌ Удалить все количество", callback_data='product all,'
                                                                             + str(order_id) + ',' + str(product_id))
    markup.row(button, button1, button2)

    return markup


@timeit
def approved_order(order_id: int) -> InlineKeyboardMarkup:
    """
    Создание кнопки для оформления заказа
    :param order_id: номера заказа
    :return:
    """
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("✔ Оформить заказ", callback_data='approved_order,' + str(order_id))
    markup.row(button)

    return markup
