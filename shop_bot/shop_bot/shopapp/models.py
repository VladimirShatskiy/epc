from django.db import models
from manage import logger
from shop_bot.settings import MEDIA_URL


@logger.catch
def path_image(instance, filename: str) -> str:
    """
    Создание пути для хранения фото

    instance: User
    filename: Имя файла
    """
    if isinstance(instance, Products):
        id_way = instance.pk
        name = 'pronunciation'
    elif isinstance(instance, Catalog):
        id_way = instance.pk
        name = 'example'
    else:
        id_way = 1
        name = "temp to delete"

    return '{media}sound {pk}/{item}/{filename}'.format(
        pk=id_way,
        filename=filename,
        item=name,
        media=MEDIA_URL
    )


class Products(models.Model):

    """
    Товары
    """
    product_name = models.CharField(max_length=50, verbose_name="Товар", null=True)
    description = models.TextField(verbose_name='Описание товара', blank=True)
    pictures = models.ImageField(upload_to=path_image, blank=True, null=True, verbose_name='Изображение товара')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"


class Catalog(models.Model):
    """
    Категория товаров
    """
    name = models.CharField(max_length=50, verbose_name="Категория", null=True)
    description = models.TextField(verbose_name='Описание категории', blank=True)
    pictures = models.ImageField(upload_to=path_image, blank=True, null=True, verbose_name='Изображение товара')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"

