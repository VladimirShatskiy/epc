from config_data.config import CUR, lock
from loader import bot
from loguru import logger

@logger.catch
def up_message(message):

    bot.unpin_all_chat_messages(message)
    data = (message,)
    with lock:
        CUR.execute("""SELECT "order", "order_type_rus" FROM users WHERE telegram_id = ?""", data)

    data = (CUR.fetchall())
    try:
        text = f'ЗН {data[0][0]} тип {data[0][1]}'
    except IndexError:
        text = f'ЗН {data[0][0]} тип не выбран'

    to_pin = bot.send_message(message, text, parse_mode="Markdown").message_id
    bot.pin_chat_message(chat_id=message, message_id=to_pin)
