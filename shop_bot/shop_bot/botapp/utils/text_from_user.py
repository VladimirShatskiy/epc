from shop_bot.settings import DEBUG

from loader import bot
from django.contrib.auth.models import User
from manage import logger


@logger.catch()
def user_text_processing(user: object, message: object):
    """
    Обработка текстового сообщения написанного User
    Отправка сообщения администраторам канала
    """

    # if DEBUG:
    #     logger.info(f"вход user_text_processing(user: {object}, message: object):")
    #
    # storages = Lease.objects.filter(user_id=user, lease_completed=False)
    # admins_telegram = Profile.objects.filter(profile_role__role_title='admin').\
    #     exclude(profile_telegram_id__isnull=True)
    #
    # storage_list = ''
    # for item in storages:
    #     storage_list += str(item.storage_id) + ', '
    #
    # for item in admins_telegram:
    #     message_text = f"Сообщение от пользователя {user.first_name} {user.last_name}\n" \
    #                    f"Арендует : {storage_list}\n" \
    #                    f"Сообщение :\n" \
    #                    f"{message.text}"
    #     bot.send_message(item.profile_telegram_id, message_text,
    #                      reply_markup=choice_user_to_answer([user, ]))
    #
    #     bot.send_message(item.profile_telegram_id,
    #                      "Для ответа пользователю выберите его нажав на кнопку и напишите ответ")
    #
    #     # Сохранение сообщения
    #     to_user = User.objects.get(profile_user_id__profile_telegram_id=item.profile_telegram_id)
    #
    #     message_to_sql(send_from=user, send_to=to_user, send_text=message.text)
    #
    # if DEBUG:
    #     logger.info("выход user_text_processing():")
