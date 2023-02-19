from telebot.types import Message
from config_data.config import CUR, lock, CONNECT_BASE
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
        CUR.execute("SELECT phone, access_level FROM users JOIN access_level \n"
                    "    ON users.user_type = access_level.type_id ")

    data = CUR.fetchall()
    text = [f'телефон:{phone} доступ: {access}' for phone, access in data]
    text = '\n'.join(text) + '\n\nДля смены уровня доступа необходимо полностью написать номер ' \
                             'телефона и через пробел указать номер уровня\n\n'
    with lock:
        CUR.execute("SELECT * FROM access_level")
    data = CUR.fetchall()
    for id, level, name, description in data:
        text += f'{id} - <b>({level}) {name}</b>\n         <i>{description}</i>\n'
    text += '\nПример: 7654321234 1'

    bot.send_message(message.from_user.id, text, parse_mode='html')
    text_message = bot.send_message(message.from_user.id,
                                    'Жду телефон с доступом или напиши "нет", для выхода из администратора')

    bot.register_next_step_handler(text_message, change_access)


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

