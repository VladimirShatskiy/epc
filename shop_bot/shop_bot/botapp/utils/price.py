from shopapp.models import OrderProduct


def total_price(order: object) -> int:

    total = 0
    items = OrderProduct.objects.filter(order=order)
    for item in items:
        total += item.count * item.price

    return total

