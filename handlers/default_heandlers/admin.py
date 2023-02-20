from telebot.types import Message
import os
import keyboards.inline.admin
from keyboards import inline
from config_data.config import CUR, lock, CONNECT_BASE, BRANCH_PHOTO
from loader import bot


@bot.message_handler(commands=['admin'])
def bot_admin(message: Message):
    """
    Админский доступ на изменение доступов владельцев телефонов
    """

    data = (message.from_user.id,)
    with lock:
        CUR.execute("SELECT access_level FROM users JOIN access_level \n"
                    "    ON users.user_type = access_level.type_id WHERE telegram_id = ?", data)

    if CUR.fetchone()[0] != "admin":
        bot.send_message(message.from_user.id, "У Вас нет доступа к данной функции")
        return

    with lock:
        CUR.execute("""SELECT main.users.name, phone, access_level  FROM users JOIN access_level \n"""
                    """    ON users.user_type = access_level.type_id """)

    data = CUR.fetchall()
    text = [f'телефон:{phone} доступ: {access}\n имя: {name}' for name, phone, access in data]
    text = '\n'.join(text) + '\n'
    bot.send_message(message.from_user.id, text, reply_markup=keyboards.inline.admin.keyboard())


def change_access(message: Message):
    if message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "Вышел из настроек")
        return
    try:
        phone, access = message.text.split(' ')
        data = (access, phone,)
        data_phone = (phone,)
        data_access = (int(access),)
        with lock:
            CUR.execute("""SELECT type_id FROM access_level WHERE type_id = ?""", data_access)
        if CUR.fetchone() is None:
            raise
        with lock:
            CUR.execute("SELECT name FROM users WHERE phone = ?", data_phone)
        if CUR.fetchone() is None:
            raise
        else:
            with lock:
                CUR.execute("""UPDATE users SET user_type = ? where phone = ?""", data)
                CONNECT_BASE.commit()
    except:
        bot.send_message(message.from_user.id, "Внесенные данные не верны,"
                                               "Уровень доступа не изменен\n"
                                               "Вышел из настроек")
    else:
        bot.send_message(message.from_user.id, "Уровень доступа изменен\n"
                                               "Вышел из настроек")


def change_level_access(message: Message):
    with lock:
        CUR.execute("SELECT * FROM access_level")
    data = CUR.fetchall()
    text = 'Для смены доступа укажи номер телефона и через пробел цифру уровня\n\n'
    for id, level, name, description in data:
        text += f'{id} - <b>({level}) {name}</b>\n         <i>{description}</i>\n\n'
    text += 'Пример: 7654321234 1'

    bot.send_message(message.from_user.id, text, parse_mode='html')
    text_message = bot.send_message(message.from_user.id,
                                    'Жду телефон с доступом или напиши "нет", для выхода из администратора')

    bot.register_next_step_handler(text_message, change_access)


def set_new_name(message: Message):
    if message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "Вышел из настроек")
        return
    phone, name = message.text.split(' ')
    data_phone = (phone,)
    data = (name, phone,)
    with lock:
        CUR.execute("""SELECT * FROM users WHERE phone = ?""", data_phone)
        if CUR.fetchone() is None:
            bot.send_message(message.from_user.id, "Номер телефона неверен, повторите попытку\n"
                                                   "Войдя в настройки заново")
        else:
            CUR.execute("""UPDATE users SET "name" = ? WHERE phone = ?""", data)
            CONNECT_BASE.commit()
            bot.send_message(message.from_user.id, "Внес изменение в имя")


def change_name(message: Message):
    bot.send_message(message.from_user.id, 'Введи номер телефона и новое имя пользователя\n'
                                           'пример 1235456445 Иван')
    text_message = bot.send_message(message.from_user.id,
                                    'Жду телефон с доступом или напиши "нет", для выхода из администратора')

    bot.register_next_step_handler(text_message, set_new_name)


def view_protokol(message: Message):
    if message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "Вышел из настроек")
        return

    file_name = 'recording_dialog_' + message.text + '.txt'
    file = os.path.join(BRANCH_PHOTO, message.text, file_name)

    try:
        with open(file, 'r', encoding='utf-8') as file_open:
            data_file = file_open.read()
    except FileNotFoundError:
        bot.send_message(message.from_user.id, 'Неверно указан номер заказ наряда '
                                               'или переписки между клиентом и сотрудником не было')

    bot.send_message(message.from_user.id, data_file)


def view_dialog(message: Message):

    text_message = bot.send_message(message.from_user.id,
                                    'Введи номер заказ наряда полностью\n'
                                    'или напиши "нет", для выхода из администратора')

    bot.register_next_step_handler(text_message, view_protokol)

