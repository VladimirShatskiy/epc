from telebot.types import Message
from config_data.config import CUR, lock
from utils import order
from loader import bot


@bot.message_handler(commands=['order'])
def bot_order(message: Message):

    data = (message.from_user.id,)
    with lock:
        CUR.execute("""SELECT active, access_level FROM users JOIN access_level 
        ON users.user_type = access_level.type_id WHERE telegram_id = ?""", data)

    data = CUR.fetchall()[0]

    print(data)

    if data[1] == "client":
        bot.send_message(message.from_user.id, "У Вас нет доступа к данной функции")
        return
    elif data[0] == 2:
        bot.send_message(message.from_user.id, "Ваш доступ заблокирован\n"
                                               "Просьба обратиться к администратору")
        return

    else:
        order.choice(message)



