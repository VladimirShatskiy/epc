from django.contrib.auth.models import User
from loguru import logger
from telebot.types import Message
from shop_bot.settings import DEBUG, MEDIA_ROOT
from botapp.config_data import config
from loader import bot

import requests
import os


# @bot.message_handler(content_types=['photo', 'video'])
# @logger.catch
# def bot_photo(message: Message):
#     if DEBUG:
#         logger.info(f"вход bot_photo(message: Message):")
#
#     if message.content_type == 'photo':
#         file_id = message.photo[-1].file_id
#         file_name = f'{file_id[:-30]}' + '.png'
#     else:
#         file_id = message.video.file_id
#         file_name = f'{file_id[:-30]}' + '.mov'
#
#     file_info = bot.get_file(file_id)
#     file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.
#                         format(config.BOT_TOKEN, file_info.file_path))
#
#     try:
#         user = User.objects.get(profile_user_id__profile_telegram_id=message.from_user.id)
#         if not user.is_active:
#             bot.send_message(message.from_user.id, "Ваш доступ заблокирован, обратитесь к администратору")
#             return
#     except User.DoesNotExist:
#         bot.send_message(message.from_user.id, "Необходимо пройти регистрацию")
#         return
#
#     # если фото от арендатора сохраняем его на портале и отправляем информацию админу
#     if user.profile_user_id.profile_role.role_title == 'user':
#
#         way = os.path.join('user {pk}'.format(pk=user.pk), 'storages')
#         full_way = os.path.join(MEDIA_ROOT, way)
#         if not os.path.isdir(full_way):
#             os.makedirs(full_way)
#
#         with open(os.path.join(full_way, file_name), 'wb') as open_file:
#             open_file.write(file.content)
#
#         Photo.objects.create(photo_path=os.path.join(way, file_name),
#                              photo_user=user)
#
#     # Если фото отправляет admin
#     elif user.profile_user_id.profile_role.role_title == 'admin':
#         bot.send_message(message.from_user.id, "Принимаю варианты на предмет что делать с этим фото, "
#                                                "надо подумать кому его высылать\n"
#                                                "или просто сохранить?\n"
#                                                "при этом оно будет сохранено как фотография от admin не понятная к чему"
#                                                "")
#
#     else:
#         bot.send_message(message.from_user.id, 'Статус пользователя неизвестен, фото не принято')
#
#     if DEBUG:
#         logger.info(f"выход bot_photo(message: Message):")
