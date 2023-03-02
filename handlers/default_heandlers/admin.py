from telebot.types import Message
import os
import keyboards.inline.admin
from config_data.config import CUR, lock, CONNECT_BASE, BRANCH_PHOTO
from loader import bot
from loguru import logger


@bot.message_handler(commands=['admin'])
@logger.catch
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
        CUR.execute("""SELECT main.users.name, phone, access_level, active  FROM users JOIN access_level \n"""
                    """    ON users.user_type = access_level.type_id """)

    data = CUR.fetchall()
    text = [f'Телефон:{phone} Имя: {name}\nДоступ: {access} Статус активности {active}' for name, phone, access, active in data]
    text = '\n'.join(text) + '\n'

    with open('users.txt', 'w', encoding='utf-8') as file:
        file.write(text)
    with open('users.txt', 'r', encoding='utf-8') as file:
        bot.send_document(message.from_user.id, file)
    text_fo_bot = "Полный список пользователей в файле\n\n" + text[:300]
    bot.send_message(message.from_user.id, text_fo_bot, reply_markup=keyboards.inline.admin.keyboard())


@logger.catch
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


@logger.catch
def change_level_access(message: Message):
    with lock:
        CUR.execute("""SELECT * FROM access_level""")
    data = CUR.fetchall()
    text = 'Для смены доступа укажи номер телефона и через пробел цифру уровня\n\n'
    for id, level, name, description in data:
        text += f'{id} - <b>({level}) {name}</b>\n         <i>{description}</i>\n\n'
    text += 'Пример: 7654321234 1'

    bot.send_message(message.from_user.id, text, parse_mode='html')
    text_message = bot.send_message(message.from_user.id,
                                    'Жду телефон с доступом или напиши "нет", для выхода из администратора')

    bot.register_next_step_handler(text_message, change_access)


@logger.catch
def set_new_name(message: Message):
    if message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "Вышел из настроек")
        return
    phone, *all = message.text.split(' ')
    name = message.text[len(phone) + 1:]
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


@logger.catch
def change_name(message: Message):
    bot.send_message(message.from_user.id, 'Введи номер телефона и новое имя пользователя\n'
                                           'Пример: 1235456445 Иван')
    text_message = bot.send_message(message.from_user.id,
                                    'Жду телефон с доступом или напиши "нет", для выхода из администратора')

    bot.register_next_step_handler(text_message, set_new_name)


@logger.catch
def view_protokol(message: Message):
    if message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "Вышел из настроек")
        return

    file_name = 'recording_dialog_' + message.text + '.txt'
    file = os.path.join(BRANCH_PHOTO, message.text, file_name)

    try:
        with open(file, 'r', encoding='utf-8') as file_open:
            data_file = file_open.read()
            bot.send_message(message.from_user.id, data_file)
    except FileNotFoundError:
        bot.send_message(message.from_user.id, 'Неверно указан номер заказ наряда '
                                               'или переписки между клиентом и сотрудником не было')


@logger.catch
def view_dialog(message: Message):

    text_message = bot.send_message(message.from_user.id,
                                    'Введи номер заказ наряда полностью\n'
                                    'или напиши "нет", для выхода из администратора')

    bot.register_next_step_handler(text_message, view_protokol)


@logger.catch
def change_active_write(message: Message):
    if message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "Вышел из настроек")
        return

    phone, active = message.text.split(' ')
    data_phone = (phone,)
    data = (active, phone,)
    with lock:
        CUR.execute("""SELECT * FROM users WHERE phone = ?""", data_phone)
        if CUR.fetchone() is None:
            bot.send_message(message.from_user.id, "Номер телефона неверен, повторите попытку\n"
                                                   "Войдя в настройки заново")
        else:
            CUR.execute("""UPDATE users SET "active" = ? WHERE phone = ?""", data)
            CONNECT_BASE.commit()
            bot.send_message(message.from_user.id, f"Внес изменение номер телефона {phone} статус {active}")


@logger.catch
def change_active(message: Message):
    text_message = bot.send_message(message.from_user.id,
                                    'Введи номер телефона пользователя и состояние активности через пробел\n'
                                    '1 - пользователь активен \n'
                                    '2 - пользователь отключен\n'
                                    'или напиши "нет", для выхода из администратора \n'
                                    'Пример: 1235456445 1')

    bot.register_next_step_handler(text_message, change_active_write)

