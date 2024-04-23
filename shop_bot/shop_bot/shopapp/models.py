from django.utils import timezone

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from manage import logger
from shop_bot.settings import MEDIA_URL
from django.db.models.signals import post_save
from django.dispatch import receiver


@logger.catch
def path_image(instance, filename: str) -> str:
    """
    Создание пути для хранения фото

    instance: User
    filename: Имя файла
    """
    if isinstance(instance, SubCatalog):
        id_way = instance.pk

        return 'subcatalog {pk}/{filename}'.format(
            pk=id_way,
            filename=filename,
            media=MEDIA_URL
        )

    elif isinstance(instance, Catalog):
        id_way = instance.pk

        return 'catalog {pk}/{filename}'.format(
            pk=id_way,
            filename=filename,
            media=MEDIA_URL
        )

    elif isinstance(instance, Images):
        id_way = instance.product_id.pk
        name = 'images'

    else:
        id_way = 1
        name = "temp to delete"

    return 'product {pk}/{item}/{filename}'.format(
        pk=id_way,
        filename=filename,
        item=name,
        media=MEDIA_URL
    )


class Catalog(models.Model):
    """
    Категория товаров
    """
    name = models.CharField(max_length=50, verbose_name="Категория", null=True)
    description = models.TextField(verbose_name='Описание категории', blank=True)
    pictures = models.ImageField(upload_to=path_image, blank=True, null=True, verbose_name='Изображение товара')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"


class SubCatalog(models.Model):
    """
    Категория товаров
    """
    name = models.CharField(max_length=50, verbose_name="Подкатегория", null=True)
    description = models.TextField(verbose_name='Описание подкатегории', blank=True)
    pictures = models.ImageField(upload_to=path_image, blank=True, null=True, verbose_name='Изображение подкатегории')
    category = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name='Категория', null=True)

    def __str__(self):
        return f'{self.category}  {self.name}'

    def __repr__(self):
        return f'{self.category}  {self.name}'

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = "Подкатегории"


class Products(models.Model):

    """
    Товары
    """
    product_name = models.CharField(max_length=50, verbose_name="Товар")
    description = models.TextField(verbose_name='Описание товара', blank=True)
    price = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100000)],
                                verbose_name="Стоимость")
    subcategory = models.ForeignKey(SubCatalog, on_delete=models.CASCADE, null=True, verbose_name="Подкатегория",
                                    related_name='subcategory')
    article = models.CharField(max_length=50, verbose_name="Артикул")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"

    def __str__(self):
        return f'{self.product_name}: артикул {self.article}'

    def __repr__(self):
        return self.product_name


class Images(models.Model):
    """
    Фотографии товаров
    """
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Товар", related_name='images')
    pictures = models.ImageField(upload_to=path_image, blank=True, null=True, verbose_name='Изображение товара')

    def __str__(self):
        return f'{self.product_id.product_name}'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = "Изображения товара"


class Feedback(models.Model):
    """
    Отзывы покупателей
    """
    text_feedback = models.TextField(verbose_name='Отзыв', blank=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Категория товара",
                                   related_name='feedback')
    author = models.ForeignKey(User, verbose_name="От пользователя", on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = "Отзывы"


class StatusOrders(models.Model):
    status = models.CharField(max_length=30, verbose_name='статус заказа')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = "Статусы"

    def __str__(self):
        return f'{self.status}'


class Orders(models.Model):
    """
    Заказы покупателей
    """
    create_by = models.ForeignKey(User, verbose_name="Клиент", on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True, verbose_name="Создан")
    status = models.ForeignKey(StatusOrders, on_delete=models.CASCADE, verbose_name='Статус',
                               related_name='orders')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'{self.pk}'


class OrderProduct(models.Model):
    """
    Модель товаров в заказе
    """
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_product_order',
                              verbose_name='Заказ')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар',
                                related_name='order_product_product')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость', default=0)
    count = models.PositiveIntegerField(default=0, verbose_name="Количество")

    def __str__(self):
        return f'Заказ {self.order} {self.product}'

    class Meta:
        verbose_name = 'товары в заказе'
        verbose_name_plural = 'товары в заказе'


class Profile(models.Model):
    """
    Профиль пользователя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    telegram = models.CharField(max_length=100, blank=True, verbose_name='ID telegram')
    phone = models.CharField(max_length=100, blank=True, verbose_name="Телефон")

    class Meta:
        verbose_name = 'Телеграмм'
        verbose_name_plural = 'Профиль в телеграмме'


# Сохранение профиля при создании или обновлении пользователя
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Автоматическое обновление Профиля пользователя при сохранении изменения в пользователе
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Messages(models.Model):
    """
    Модель сообщений пользователей

    message_from: User от кого получено сообщение
    message_to: User кому отослано сообщение
    message_date: дата сообщения
    message_text: текст сообщения
    """

    message_from = models.ForeignKey(User, on_delete=models.PROTECT,
                                     related_name='user_message_from', verbose_name='Сообщение от',
                                     default=1, null=False)
    message_to = models.ForeignKey(User, on_delete=models.PROTECT,
                                   related_name='user_message_to', verbose_name='Сообщение для', null=False)
    message_date = models.DateTimeField(default=timezone.now, verbose_name='Дата сообщения')
    message_text = models.TextField(verbose_name="Сообщение", blank=False, null=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = "сообщения"

    def __repr__(self):
        return self.message_to, self.message_text, self.message_from

    def __str__(self):
        return f'{str(self.message_text)[:10]} ... '


class MessagesId(models.Model):
    """
    Модель хранения ID сообщений пользователей
    """

    telegram_id = models.IntegerField(verbose_name="Телеграм пользователя")
    messages_id = models.IntegerField(verbose_name='id сообщения')
    item = models.CharField(max_length=10, default=None)
    url = models.CharField(max_length=100, blank=True, null=True, verbose_name='url')

    def __str__(self):
        return self.messages_id


