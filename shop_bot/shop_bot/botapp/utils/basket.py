from django.contrib.auth.models import User
from loguru import logger
from telebot.apihelper import ApiTelegramException
from telebot.types import Message

from botapp.keyboards.inline.basket import plus_minus, approved_order, put_basket
from botapp.utils.decorators import timeit
from botapp.utils.message import message_add_to_sql, message_delete

from botapp.utils.price import total_price
from botapp.utils.product import text_description
from botapp.utils.text import show_description_order_product, text_total_price
from loader import bot
from shop_bot.settings import MY_DEBUG
from shopapp.models import Products, OrderProduct, Orders, StatusOrders, MessagesId


@timeit
@logger.catch
def add_product_in_order(message: Message, product_id: int, message_id_to_edit: int) -> None:
    """
    Добавление товара в заказ
    :param message_id_to_edit: номер сообщения для редактирования
    :param message: Message telegram
    :param product_id: ID товара
    :return: None
    """

    if MY_DEBUG:
        logger.info(f"вход: add_product_in_order(message: Message, product_id: int, message_id_to_edit: int),"
                    f"{product_id} , {message_id_to_edit}")

    product = Products.objects.get(pk=product_id)
    user = User.objects.get(profile__telegram=message.from_user.id)

    try:
        order = Orders.objects.get(create_by=user,
                                   status=StatusOrders.objects.get(status='Корзина'))
    except Orders.DoesNotExist:
        order = Orders.objects.create(create_by=user,
                                      status=StatusOrders.objects.get(status='Корзина'))

    OrderProduct.objects.get_or_create(order=order, product=product)
    put_product = OrderProduct.objects.get(order=order, product=product)
    put_product.count += 1
    put_product.price = product.price
    put_product.save()

    try:
        bot.edit_message_caption(caption=text_description(product=product,
                                                          put_product=put_product),
                                 chat_id=message.from_user.id,
                                 message_id=message_id_to_edit,
                                 reply_markup=put_basket(message, product_id=product.pk))
    except ApiTelegramException:
        bot.edit_message_text(text=text_description(product=product,
                                                    put_product=put_product),
                              chat_id=message.from_user.id,
                              message_id=message_id_to_edit,
                              reply_markup=put_basket(message, product_id=product.pk))

    if MY_DEBUG:
        logger.info(f"выход: add_product_in_order(message: Message, product_id: int, message_id_to_edit: int),")


@timeit
@logger.catch
def show_order(message: Message, order_id: int = None) -> None:
    """
    Отображение содержимого корзины
    :param order_id: номер заказа
    :param message:
    :return:
    """

    if MY_DEBUG:
        logger.info(f"вход: show_order(message: Message)")

    total_basket = 0
    message_delete(message.from_user.id)
    if not order_id:
        try:
            order = Orders.objects.get(
                create_by=User.objects.get(username=message.from_user.id),
                status=StatusOrders.objects.get(status="Корзина"))

        except Orders.DoesNotExist:
            message_add_to_sql(
                bot.send_message(message.from_user.id, text="На данный момент корзина пуста\n"
                                                            "Начнете с добавления товаров")
            )
            return

        products = OrderProduct.objects.filter(order=order)
    else:
        order = Orders.objects.get(pk=order_id)
        products = OrderProduct.objects.filter(order=order)

    message_add_to_sql(
        bot.send_message(message.from_user.id, text="Полный список товаров в заказе")
    )

    for product in products:
        msg = bot.send_message(message.from_user.id,
                               text=show_description_order_product(product),
                               reply_markup=plus_minus(order_id=order.pk,
                                                       product_id=product.product_id))
        message_add_to_sql(msg)
        total_basket += product.price * product.count

    message_add_to_sql(
        bot.send_message(message.from_user.id,
                         text=text_total_price(total_price(order)),
                         reply_markup=approved_order(order.pk))
    )

    if MY_DEBUG:
        logger.info(f"выход: show_order(message: Message)")


def product_plus(order_id: int, product_id: int, message: Message):
    """
    Добавление продукта к заказу
    :param message:
    :param order_id:
    :param product_id:
    :return:
    """

    if MY_DEBUG:
        logger.info(f'вход: product_plus(order_id: int, product_id: int, message: Message)'
                    f'{order_id} {product_id}')

    order = Orders.objects.get(pk=order_id)

    item = OrderProduct.objects.get(order=order,
                                    product=Products.objects.get(pk=product_id))

    item.count += 1
    item.save()

    bot.edit_message_text(text=show_description_order_product(item),
                          chat_id=message.from_user.id,
                          message_id=message.message.id,
                          reply_markup=plus_minus(order_id=order_id, product_id=product_id))

    message_id = MessagesId.objects.filter(telegram_id=message.from_user.id).latest('messages_id').messages_id

    bot.edit_message_text(text=text_total_price(total_price(order)),
                          chat_id=message.from_user.id,
                          message_id=int(message_id),
                          reply_markup=approved_order(order.pk))
    if MY_DEBUG:
        logger.info(f'выход: product_plus(order_id: int, product_id: int, message: Message)'
                    f'{order_id} {product_id}')


def product_minus(order_id: int, product_id: int, message: Message):
    """
    Удаление продукта из заказа
    :param message:
    :param order_id:
    :param product_id:
    :return:
    """

    if MY_DEBUG:
        logger.info(f'вход: product_minus(order_id: int, product_id: int, message: Message)'
                    f'{order_id} {product_id}')

    order = Orders.objects.get(pk=order_id)

    item = OrderProduct.objects.get(order=order,
                                    product=Products.objects.get(pk=product_id))
    if item.count == 1:
        item.delete()
        bot.delete_message(chat_id=message.from_user.id, message_id=message.message.id)
    else:
        item.count -= 1
        item.save()

        bot.edit_message_text(text=show_description_order_product(item),
                              chat_id=message.from_user.id, message_id=message.message.id,
                              reply_markup=plus_minus(order_id=order_id, product_id=product_id))

        message_id = MessagesId.objects.filter(telegram_id=message.from_user.id).latest('messages_id').messages_id

        bot.edit_message_text(text=text_total_price(total_price(order)),
                              chat_id=message.from_user.id,
                              message_id=int(message_id),
                              reply_markup=approved_order(order_id))
    if MY_DEBUG:
        logger.info(f'выход: product_minus(order_id: int, product_id: int, message: Message)'
                    f'{order_id} {product_id}')


def product_minus_all(order_id: int, product_id: int, message: Message):
    """
    Удаление всей линии товара из заказа
    :param order_id:
    :param product_id:
    :param message:
    :return:
    """

    if MY_DEBUG:
        logger.info(f'вход: product_minus_all(order_id: int, product_id: int, message: Message):'
                    f'{order_id} {product_id}')

    order = Orders.objects.get(pk=order_id)

    item = OrderProduct.objects.get(order=order,
                                    product=Products.objects.get(pk=product_id))
    item.delete()
    bot.delete_message(chat_id=message.from_user.id, message_id=message.message.id)

    message_id = MessagesId.objects.filter(telegram_id=message.from_user.id).latest('messages_id').messages_id

    bot.edit_message_text(text=text_total_price(total_price(order)),
                          chat_id=message.from_user.id,
                          message_id=int(message_id),
                          reply_markup=approved_order(order_id))
    if MY_DEBUG:
        logger.info(f'выход: product_minus_all(order_id: int, product_id: int, message: Message):'
                    f'{order_id} {product_id}')
