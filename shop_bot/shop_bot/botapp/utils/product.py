import os

from django.contrib.auth.models import User
from telebot.types import Message

from botapp.keyboards.inline.basket import put_basket
from botapp.utils.decorators import timeit
from botapp.utils.message import message_add_to_sql
from loader import bot
from manage import logger
from shop_bot.settings import MY_DEBUG, MEDIA_URL
from shopapp.models import Products, Images, Orders, StatusOrders, OrderProduct


@timeit
@logger.catch()
def text_description(product: object, put_product: object = None) -> str:
    """
    Формирование текста для описания товара
    :param put_product:
    :param product:
    :return:
    """
    text_out = f'Наименование: {product.product_name}\n' \
               f'Артикул: {product.article}\n' \
               f'Описание: {product.description}\n' \
               f'Стоимость: {product.price}\n'
    if put_product:
        if put_product.count > 0:
            text_out += f'Количество в корзине: {put_product.count}'
    return text_out


@timeit
@logger.catch()
def show_product_with_category(message: Message, subcategory: int) -> None:
    """
    Вывод информации о товаре в зависимости от подкатегории товара
    :param message: message telegram
    :param subcategory: ID подкатегории товара
    :return:
    """
    if MY_DEBUG:
        logger.info(f"начало: show_product_with_category(message: Message{message.from_user.id},"
                    f" subcategory: int {subcategory}) ")

    products = Products.objects.filter(subcategory_id=subcategory)

    show_products(products=products, message=message)

    if MY_DEBUG:
        logger.info(f"выход : show_product_with_category(message: Message subcategory: int) ")


@timeit
@logger.catch()
def show_products(products: list[object], message: Message) -> None:

    if MY_DEBUG:
        logger.info(f"вход : show_products(products: list[object], message: Message)")

    user = User.objects.get(profile__telegram=message.from_user.id)

    try:
        order = Orders.objects.get(create_by=user,
                                   status=StatusOrders.objects.get(status='Корзина'))
    except Orders.DoesNotExist:
        order = None

    for product in products:

        # по возможности переделать, сделать выгрузку одним запросом
        images = Images.objects.filter(product_id=product.pk)

        # добавляем текст к последней фотографии из всех по товару
        for image in images[1:]:
            if image.pictures:
                way = os.path.join(MEDIA_URL, str(image.pictures))
                img = open(way, 'rb')
                message_add_to_sql(
                    bot.send_photo(message.from_user.id, photo=img)
                )
        try:
            if order:
                try:
                    put_product = OrderProduct.objects.get(order=order, product=product)
                except OrderProduct.DoesNotExist:
                    put_product = None
            else:
                put_product = None
            if images[0].pictures:
                way = os.path.join(MEDIA_URL, str(images[0].pictures))
                img = open(way, 'rb')

                message_add_to_sql(
                    bot.send_photo(message.from_user.id,
                                   photo=img,
                                   caption=text_description(product, put_product),
                                   reply_markup=put_basket(message=message,
                                                           product_id=product.pk))
                )
        except IndexError:
            if order:
                try:
                    put_product = OrderProduct.objects.get(order=order, product=product)
                except OrderProduct.DoesNotExist:
                    put_product = None
            else:
                put_product = None

            message_add_to_sql(
                bot.send_message(message.from_user.id,
                                 text_description(product, put_product),
                                 reply_markup=put_basket(message=message,
                                                         product_id=product.pk))
            )