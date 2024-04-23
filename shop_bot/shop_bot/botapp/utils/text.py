

def show_description_order_product(item: object) -> str:
    """
    Вывод информации о товаре из заказа
    :param item:
    :return:
    """
    text = f'Наименование: {item.product}\n' \
           f'Количество: {item.count}\n' \
           f'стоимость за единицу: {item.price}\n' \
           f'Стоимость итого: {item.price * item.count} руб.\n'

    return text


def text_total_price(total: int) -> str:
    return f"Общая сумма заказа {total} руб\n" \
           f"В случае согласия подтвердите оформление заказа"
