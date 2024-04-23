from django import forms

from loader import bot
from shopapp.models import OrderProduct, Products, Messages


class OrdersProductAdminForm(forms.ModelForm):
    model = OrderProduct

    def clean(self):
        cleaned_data = self.cleaned_data
        product_id = cleaned_data.get('product')
        get_price = cleaned_data.get('price')

        if get_price == 0.00 or get_price == 0:
            price = Products.objects.get(pk=product_id.pk).price
            self.cleaned_data["price"] = price

        return self.cleaned_data


class MessagesAdminForm(forms.ModelForm):

    model = Messages

    def clean(self):
        """
        Отправка сообщения пользователю при сохранении
        """

        cleaned_data = self.cleaned_data

        text_message = cleaned_data.get('message_text')
        user = cleaned_data.get('message_to')

        if not user:
            raise forms.ValidationError(f"Необходимо указать кому отправляется сообщение")

        # если это редактирование сообщения, то сообщение в бот не отправляется
        if not self.instance.pk:
            text_for_telegram = f'Сообщение от администратора портала\n' \
                                f'{text_message}'
            bot.send_message(user.profile.telegram, text_for_telegram)

        return cleaned_data

    def newform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['show_delete'] = False
        # extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        # extra_context['show_save_and_add_another'] = False

        return super().changeform_view(request, object_id, form_url, extra_context)
