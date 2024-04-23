from loguru import logger

from botapp.utils.decorators import timeit
from botapp.utils.message import message_delete, message_add_to_sql
from botapp.utils.product import show_products
from loader import bot
from telebot.types import Message

from shop_bot.settings import MY_DEBUG
from shopapp.models import Products


@timeit
@logger.catch()
def search_product_by_string(message: Message) -> None:
    """
    Поиск и выводи в виде меню всех продуктов по совпадению слов в названии, описании и артикулу
    :param message:
    :return:
    """

    if MY_DEBUG:
        logger.info(f'вход: search_product_by_string(message: Message)')

        msg = bot.send_message(message.chat.id, 'Введите текст для поиска')
        message_add_to_sql(msg)

        bot.register_next_step_handler(msg, input_search_string)

    if MY_DEBUG:
        logger.info(f'вход: search_product_by_string(message: Message)')


@timeit
@logger.catch()
def input_search_string(message: Message) -> None:
    """
    Перехватчик ввода текста для поиска продукта
    :param message:
    :return:
    """

    from django.db.models import Q

    bot.delete_message(message.chat.id, message.message_id)
    message_delete(message.from_user.id)

    text = message.text
    b_text = text.capitalize()

    products = Products.objects.filter(
        Q(product_name__icontains=text) |
        Q(article__icontains=text) |
        Q(product_name__icontains=b_text) |
        Q(article__icontains=b_text)
    )

    show_products(products, message)
