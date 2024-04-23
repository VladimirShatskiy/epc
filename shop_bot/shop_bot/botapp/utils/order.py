from django.contrib.auth.models import User
from loguru import logger
from telebot.types import Message

from botapp.keyboards.inline.orders import all_orders
from botapp.utils.decorators import timeit
from botapp.utils.message import message_add_to_sql, message_delete
from loader import bot
from shop_bot.settings import MY_DEBUG
from shopapp.models import OrderProduct, Orders, StatusOrders, Profile


@timeit
@logger.catch
def approve_order(order_id: int, message: Message) -> None:
    """
    Подтверждение создания заказа и извещение админов о созданном заказе
    :param order_id:
    :param message:
    :return:
    """

    if MY_DEBUG:
        logger.info(f"вход : approve_order(order_id: int, message: Message) {order_id} ")

    message_delete(message.from_user.id)

    order = Orders.objects.get(pk=order_id)
    order.status = StatusOrders.objects.get(status="Оформлен")
    order.save()

    message_add_to_sql(
        bot.send_message(message.from_user.id, text="Ваш заказ оформлен и принят в обработку\n"
                                                    "оператор свяжется с Вами в ближайшее время")
    )

    admins = Profile.objects.filter(user__is_staff=True)

    user = User.objects.get(profile__telegram=message.from_user.id)

    list_products = ""

    products = OrderProduct.objects.filter(order=Orders.objects.get(pk=order_id))
    total_price = 0

    for product in products:
        list_products += f'{product.product} \n' \
                         f'Количество {product.count}\n' \
                         f'Общая стоимость {product.count * product.price}\n'
        total_price += product.count * product.price

    for admin in admins:
        text = f'Клиент {user.first_name} оформил заказ № {order_id}\n' \
               f'Телефон для связи {user.profile.phone}\n' \
               f'Товары в заказе на общую сумму: {total_price} руб.\n' \
               f'                  =-* заказ *=-     \n' \
               + list_products

        message_add_to_sql(
            bot.send_message(admin.telegram, text)
        )

    if MY_DEBUG:
        logger.info(f"выход : approve_order(order_id: int, message: Message)")


@timeit
@logger.catch
def get_all_orders(message: Message) -> None:
    orders = Orders.objects.filter(create_by=User.objects.get(profile__telegram=message.from_user.id))

    if orders:
        message_add_to_sql(
            bot.send_message(message.from_user.id,
                             text="Просьба выбрать заказ для просмотра",
                             reply_markup=all_orders(orders))
        )
    else:
        message_add_to_sql(
            bot.send_message(message.from_user.id,
                             text="Заказы не найдены")
        )
