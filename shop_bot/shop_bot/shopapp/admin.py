
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from shopapp.form import OrdersProductAdminForm, MessagesAdminForm
from shopapp.models import Catalog, SubCatalog, Products, Feedback, Images, StatusOrders, Orders, OrderProduct, Profile, \
    Messages

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from django.contrib import admin, messages


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    """
    Представление каталога
    """
    list_display = ('name',
                    'description',
                    'pictures',
                    )


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    readonly_fields = [
        'date_joined',
    ]
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'telegram_id')

    @staticmethod
    def telegram_id(instance):
        return instance.profile.telegram


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)


@admin.register(SubCatalog)
class SubCatalogAdmin(admin.ModelAdmin):
    """
    Представление подкатегорий каталога
    """
    list_display = ('name',
                    'category',
                    'description',
                    'pictures',
                    )

    fieldsets = (
        (
            'Категория',
            {'fields': ('category',)}
        ),
        (
            "Подкатегория",
            {'fields': ('name', 'description', 'pictures',)}
        ),

    )


class ImagesLine(admin.TabularInline):
    model = Images


def update_prices(modeladmin, request, queryset):
    product_ids = queryset.values_list('id', flat=True)
    print(product_ids)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    """
    Представление товаров
    """
    list_display = ('product_name',
                    'article',
                    'price',
                    'images_url',
                    'feedback_show',
                    'description',
                    'sub_cat'
                    )
    inlines = [ImagesLine, ]
    actions = [update_prices]
    fieldsets = (
        (
            "Подкатегория",
            {'fields': ('subcategory', )}
        ),

        (
            "Товар",
            {'fields': ('product_name', 'article', 'price', 'description', )}
        ),
    )

    def sub_cat(self, obj):
        return obj.subcategory

    sub_cat.short_description = 'Категория товара'

    def images_url(self, obj):
        count = obj.images.count()
        url = (
                reverse("admin:shopapp_images_changelist")
                + "?"
                + urlencode({"product_id": obj.id})
        )
        return format_html('<b><a  href="{}">{}  </a></b>', url, count)

    images_url.short_description = 'Количество изображений'

    def feedback_show(self, obj):
        count = obj.feedback.count()
        url = (
                reverse("admin:shopapp_feedback_changelist")
                + "?"
                + urlencode({"product__id": obj.id})
        )
        return format_html('<b><a href="{}">{} </a></b>', url, count)

    feedback_show.short_description = 'Количество отзывов'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Представление товаров
    """
    list_display = ('text_feedback',
                    'author',
                    'product_id',
                    )


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    """
    Представление товаров
    """
    list_display = ('product_id',
                    'image_show',
                    'pictures',
                    )

    def sub_cat(self, obj):
        return obj.product_id.subcategory

    sub_cat.short_description = 'Товар относится к группе'

    def image_show(self, obj):
        if obj.pictures:
            url = (
                    reverse("admin:shopapp_images_changelist")
                    + "?"
                    + urlencode({"product__id": obj.id})
            )
            return format_html("<a href={}> <img src={} width='60' />".format(url, obj.pictures.url))

    image_show.short_description = 'Изображение'


# @admin.register(StatusOrders)
# class StatusOrdersAdmin(admin.ModelAdmin):
#     """
#     Статус заказов
#     """
#     list_display = (
#                     'status',
#                     )


@admin.register(OrderProduct)
class OrdersProductAdmin(admin.ModelAdmin):
    """
    Товары в заказе
    """
    list_display = (
                    'product',
                    'price',
                    'count',
                    'total',
                    'order',
                    )

    form = OrdersProductAdminForm

    @staticmethod
    def total(obj):
        return obj.price * obj.count


class OrdersProductLine(admin.TabularInline):
    model = OrderProduct
    form = OrdersProductAdminForm


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    """
    Заказы
    """
    list_display = ('id',
                    'create_by',
                    'product_count',
                    'total',
                    'create_at',
                    'status',
                    )
    list_filter = ['status', ]

    # def render_change_form(self, request, context, obj=None, * args, ** kwargs):
    #     self.change_form_template = 'change_form_help_text.html'
    #
    #     extra = {
    #         'help_text': "👉 При вводе стоимости товара 0, стоимость товара будет подгружена из карточки "
    #                      "товара. В случае указания стоимости вручную, в заказ будет перенесена "
    #                      "стоимость внесенная вручную 👈"
    #         }
    #     context.update(extra)
    #     return super().render_change_form(request, context, * args, ** kwargs)

    inlines = [OrdersProductLine, ]

    def total(self, obj):
        items = OrderProduct.objects.filter(order=obj.id)

        count = 0
        for item in items:
            count += item.price * item.count

        return format_html('<b>{} </b>', count)

    total.short_description = 'Сумма заказа'
    total.message_text = 'Indicates if the author is under 18.'

    def product_count(self, obj):

        all_products = 0
        counts = OrderProduct.objects.filter(order=obj.id)
        for count in counts:
            all_products += count.count

        url = (
                reverse("admin:shopapp_orderproduct_changelist")
                + "?"
                + urlencode({"order__id": obj.id})
        )
        return format_html('<b><a href="{}">{} </a></b>', url, all_products)

    product_count.short_description = 'Количество товаров в заказе'


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    """
    Вывод сообщений от пользователей в админку
    """
    list_display = ['message_text', 'message_from', 'message_to', 'message_date']
    search_fields = ['message_text', ]
    form = MessagesAdminForm

    # показываем пользовательское сообщение
    def save_model(self, request, obj, form, change):
        if not change:
            messages.add_message(request, messages.WARNING, 'Сообщение отправлено пользователю в Telegram')
        else:
            messages.add_message(request, messages.WARNING,
                                 'Отредактированные сообщения не подлежат повторной отправке')
        super(MessagesAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description="для")
    def _to(self, obj):
        return f"{obj.message_to.first_name} {obj.message_to.last_name}"

    @admin.display(description="Сообщение от")
    def _from(self, obj):
        return f"{obj.message_from.first_name} {obj.message_from.last_name}"



