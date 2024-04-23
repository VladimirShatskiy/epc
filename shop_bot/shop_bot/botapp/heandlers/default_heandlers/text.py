from django.contrib.auth.models import User
from loader import bot

from manage import logger
from botapp.utils.text_from_admin import admin_text_processing
from botapp.utils.text_from_user import user_text_processing
from shop_bot.settings import DEBUG


@logger.catch
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if DEBUG:
        logger.info(f"вход @bot.message_handler(content_types=['text'])= {message.text}")

    user = User.objects.get(profile_user_id__profile_telegram_id=message.from_user.id)

    # Сообщение от пользователя, уходит админам с указанием клиента и кладовок
    if user.profile_user_id.profile_role.role_title == 'user':
        user_text_processing(user=user, message=message)

    # Обработка сообщения если админ
    elif user.profile_user_id.profile_role.role_title == 'admin':
        admin_text_processing(user=user, message=message)

    else:
        bot.send_message(message.from_user.id, "Неизвестный тип пользователя")

    if DEBUG:
        logger.info("выход @bot.message_handler()")
