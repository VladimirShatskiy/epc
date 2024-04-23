from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from manage import logger
from shopapp.models import Catalog, SubCatalog


@logger.catch
def product_groups() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры каталога
    """

    catalog = Catalog.objects.all()

    markup = InlineKeyboardMarkup()
    for item in catalog:
        button = f'{item.name}'
        button = InlineKeyboardButton(button,
                                      callback_data='catalog_item,' +
                                                    str(item.pk)
                                      )
        markup.row(button)

    return markup


@logger.catch
def sub_product_groups(group: id) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры подкаталога
    :param group: номер группы каталога

    """

    sub_catalog = SubCatalog.objects.filter(category=group)

    markup = InlineKeyboardMarkup()
    for item in sub_catalog:
        button = f'{item.name}'
        button = InlineKeyboardButton(button,
                                      callback_data='sub_catalog_item,' +
                                                    str(item.pk)
                                      )
        markup.row(button)

    return markup
