from django.contrib.auth.models import User

from botapp.utils.message import message_to_sql
from shop_bot.settings import DEBUG

from loader import bot
from manage import logger


@logger.catch()
def admin_text_processing(user: object, message: object):
    """
    Обработка текстового сообщения написанного User
    Отправка сообщения администраторам канала
    user: User
    message: Message
    """

    if DEBUG:
        logger.info(f"вход user_text_processing(user: object ={user}, message: object):={message.from_user.id}")
        text = f'Сообщение от администратора {user.first_name}\n' \
               f'{message.text}'

        telegram_id = User.objects.get(username=user.profile_user_id.profile_answer_to).\
            profile_user_id.profile_telegram_id

        bot.send_message(telegram_id, text)

        to_user = User.objects.get(profile_user_id__profile_telegram_id=telegram_id)

        message_to_sql(send_from=user, send_to=to_user, send_text=message.text)

    if DEBUG:
        logger.info(f"выход user_text_processing()")


