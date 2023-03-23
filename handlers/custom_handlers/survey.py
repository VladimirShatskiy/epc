from config_data.config import CUR, CONNECT_BASE,  lock
from keyboards.contact import request_contact
from loader import bot
from states.contact_info import UserInfo
from telebot.types import Message, ReplyKeyboardRemove


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    """
    Получение подтверждения клиента по номеру телефона
    :param message:
    :return: None
    """
    bot.set_state(message.from_user.id, UserInfo.phone_number)  # , message.chat.id)
    bot.send_message(message.from_user.id, f'{message.from_user.full_name}\n'
                                           f'Для начала работы, просьба подтвердить свой номер телефона\n'
                                           f'👇👇👇   нажав на кнопку   👇👇👇',
                     reply_markup=request_contact())


@bot.message_handler(content_types=['contact', 'text'], state=UserInfo.phone_number)
def get_contact(message: Message) -> None:
    """
    Опрос, получение названия города и окончание опроса
    :param message:
    :return:
    """
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number

            bot.send_message(message.from_user.id, 'Спасибо за подтверждение\n'
                                                   'бот готов к работе 👍',
                             reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, None)
            data_update = (data['phone_number'], message.from_user.id, 1, 3)
            userid = (message.from_user.id,)
            with lock:
                CUR.execute("SELECT EXISTS(SELECT user_type FROM users WHERE telegram_id = ?)", userid)
            client = CUR.fetchone()
            if client[0] == 0:
                with lock:
                    CUR.execute("""INSERT INTO users (phone, telegram_id, active, user_type) VALUES (?,?,?,?)""", data_update)
                    CONNECT_BASE.commit()

    elif message.text.lower() == 'нет':
        bot.send_message(message.from_user.id, "Заполнение анкеты прервано\n"
                                               "У вас нет доступа к боту 😰", reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, None)
    else:

        bot.send_message(message.from_user.id, "Для отправки номера необходимо нажать на кнопку\n"
                                               "Или напишите 'нет' для завершения регистрации\n"
                                               "👇👇👇 кнопка ниже 👇👇👇")









