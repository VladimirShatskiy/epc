from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS, CUR, lock, CONNECT_BASE
from loader import bot


@bot.message_handler(commands=['admin'])
def bot_admin(message: Message):
    """
    Админский доступ на изменение доступов владельцев телефонов
    """

    data = (message.from_user.id,)
    lock.acquire(True)
    CUR.execute("""SELECT access_level FROM users JOIN access_level 
    ON users.user_type = access_level.type_id WHERE telegram_id = ?""", data)
    lock.release()

    if CUR.fetchone()[0] != "admin":
        bot.send_message(message.from_user.id, "У Вас нет доступа к данной функции")
        return

    lock.acquire(True)
    CUR.execute("""SELECT phone, access_level FROM users JOIN access_level 
    ON users.user_type = access_level.type_id """)
    lock.release()
    data = CUR.fetchall()
    text = [f'телефон:{phone} доступ: {access}' for phone, access in data]
    text = '\n'.join(text) + '\n\nДля смены уровня доступа необходимо полностью написать номер ' \
                             'телефона и через пробел указать уровень\n\n' \
                             '1 - <b>администратор бота</b>\n' \
                             '       <i>возможность давать доступ, фото фиксация</i>\n' \
                             '2 - <b>сотрудник сервисной станции</b>\n' \
                             '       <i>возможность фото фиксации</i>\n' \
                             '3 - <b>клиент</b>\n' \
                             '       <i>только получение фото</i>\n\n' \
                             'Пример: 7654321234 1'
    bot.send_message(message.from_user.id, text, parse_mode='html')
    text_message = bot.send_message(message.from_user.id,
                                    'Жду телефон с доступом или напиши "нет", для выхода из администратора')
    bot.register_next_step_handler(text_message, change_access)


def change_access(message: Message):
    if message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "Вышел из настроек")
        return
    try:
        lock.acquire(True)
        phone, access = message.text.split(' ')
        data = (access, phone,)
        data_phone = (phone,)
        CUR.execute("SELECT name FROM users WHERE phone = ?", data_phone)
        if CUR.fetchone() is None:
            raise
        else:
            CUR.execute("""UPDATE users SET user_type = ? where phone = ?""", data)
            CONNECT_BASE.commit()
    except:
        bot.send_message(message.from_user.id, "Внесенные данные не верны,"
                                               "Уровень доступа не изменен\n"
                                               "Вышел из настроек")
    else:
        bot.send_message(message.from_user.id, "Уровень доступа изменен\n"
                                               "Вышел из настроек")
    finally:
        lock.release()

