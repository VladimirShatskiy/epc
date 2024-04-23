from django.contrib.auth.models import User
from telebot.types import Message, ReplyKeyboardRemove
from botapp.keyboards.contact import request_contact
from botapp.states.contact_info import UserInfo
from botapp.utils.message import message_add_to_sql, message_delete

from loader import bot

from manage import logger
from shop_bot.settings import DEBUG
from shopapp.models import Profile


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    """
    Получение подтверждения клиента по номеру телефона
    :param message:
    :return: None
    """
    if DEBUG:
        logger.info("начало @bot.message_handler(commands=['survey'])")
    bot.set_state(message.from_user.id, UserInfo.phone_number)
    message_add_to_sql(
        bot.send_message(message.from_user.id, f'{message.from_user.full_name}\n'
                                               f'Для начала работы, просьба зарегистрироваться\n'
                                               f'👇👇👇   нажав на кнопку   👇👇👇',
                         reply_markup=request_contact())
    )

    if DEBUG:
        logger.info("конец @bot.message_handler(commands=['survey'])")


@bot.message_handler(content_types=['contact'], state=UserInfo.phone_number)
@logger.catch
def get_contact(message: Message) -> None:
    """
    Опрос, получение названия города и окончание опроса
    :param message:
    :return:
    """
    if DEBUG:
        logger.info("начало @bot.message_handler(content_types=['contact'], state=UserInfo.phone_number)")

    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
            data['first_name'] = message.contact.first_name

            bot.delete_message(message.chat.id, message.message_id)
            message_delete(message.from_user.id)

            message_add_to_sql(
                bot.send_message(message.from_user.id, 'Спасибо за подтверждение 👍\n'
                                                       '👇 откройте меню',
                                 reply_markup=ReplyKeyboardRemove())
            )
            bot.set_state(message.from_user.id, None)
            userid = (message.from_user.id,)

            User.objects.get_or_create(username=userid[0], first_name=data['first_name'])
            user = User.objects.get(username=userid[0])
            profile = Profile.objects.get(user=user)
            profile.phone = str(data['phone_number'])
            profile.telegram = userid[0]
            profile.save()

    elif message.text.lower() == 'нет':
        message_add_to_sql(
            bot.send_message(message.from_user.id, "Заполнение анкеты прервано\n"
                                                   "У вас нет доступа к боту 😰", reply_markup=ReplyKeyboardRemove())
        )
        bot.set_state(message.from_user.id, None)
    else:

        message_add_to_sql(
            bot.send_message(message.from_user.id, "Для регистрации необходимо нажать на кнопку\n"
                                                   "Или напишите 'нет' для отмены регистрации\n"
                                                   "👇👇👇 кнопка ниже 👇👇👇")
        )

    if DEBUG:
        logger.info("конец @bot.message_handler(content_types=['contact'], state=UserInfo.phone_number)")
