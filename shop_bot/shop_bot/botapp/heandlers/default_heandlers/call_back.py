from botapp.keyboards.inline.catalog import sub_product_groups
from botapp.utils.basket import add_product_in_order, show_order, product_plus, product_minus, product_minus_all
from botapp.utils.message import message_delete, message_add_to_sql
from botapp.utils.order import approve_order

from botapp.utils.product import show_product_with_category
from loader import bot
from manage import logger

from shop_bot.settings import DEBUG


@bot.callback_query_handler(func=lambda call: True)
@logger.catch
def callback_query(call) -> None:
    """
    Сборщик ответов всех кнопок
    :param call: message telegram
    :return: None
    """

    if DEBUG:
        logger.info(f"вход def callback_query(call):={call.data}")

    data_split = call.data.split(',')

    if data_split[0] == "catalog_item":
        message_delete(call.from_user.id)

        message_add_to_sql(
            bot.send_message(call.from_user.id, text="Выбери подгруппу товара",
                             reply_markup=sub_product_groups(data_split[1]))
        )

    elif data_split[0] == 'sub_catalog_item':
        message_delete(call.from_user.id)
        show_product_with_category(call, data_split[1])

    elif data_split[0] == 'basket':
        show_order(call)

    elif data_split[0] == 'put_basket':
        add_product_in_order(message=call, product_id=data_split[1], message_id_to_edit=call.message.id)

    elif data_split[0] == 'product +':
        product_plus(order_id=data_split[1], product_id=data_split[2], message=call)

    elif data_split[0] == 'product -':
        product_minus(order_id=data_split[1], product_id=data_split[2], message=call)

    elif data_split[0] == 'product all':
        product_minus_all(order_id=data_split[1], product_id=data_split[2], message=call)

    elif data_split[0] == 'approved_order':
        approve_order(order_id=data_split[1], message=call)

    elif data_split[0] == 'get_order_by_number':
        show_order(message=call, order_id=data_split[1])
