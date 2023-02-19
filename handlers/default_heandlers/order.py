from telebot.types import Message
from config_data.config import CUR, lock
from utils import order
from loader import bot


@bot.message_handler(commands=['order'])
def bot_order(message: Message):

    data = (message.from_user.id,)
    with lock:
        CUR.execute("""SELECT access_level FROM users JOIN access_level 
        ON users.user_type = access_level.type_id WHERE telegram_id = ?""", data)

    if CUR.fetchone()[0] == "client":
        bot.send_message(message.from_user.id, "У Вас нет доступа к данной функции")
        return
    order.choice(message)
