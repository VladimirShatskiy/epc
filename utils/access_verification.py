from functools import wraps
from config_data.config import lock, CUR
from loader import bot


def access_verification(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        message = args[0]
        data = (message.from_user.id,)
        with lock:
            CUR.execute("""SELECT active, access_level FROM users JOIN access_level 
            ON users.user_type = access_level.type_id WHERE telegram_id = ?""", data)

        data = CUR.fetchall()[0]

        if data[1] == "client":
            bot.send_message(message.from_user.id, "У Вас нет доступа к данной функции")
            return
        elif data[0] == 2:
            bot.send_message(message.from_user.id, "Ваш доступ заблокирован\n"
                                                   "Просьба обратиться к администратору")
            return

        else:
            return func(*args, **kwargs)

    return wrapper
