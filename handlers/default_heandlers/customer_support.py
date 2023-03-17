from telebot.types import Message
from config_data.config import CUR, lock
from handlers.default_heandlers.text import record_message
from loader import bot
from keyboards.inline import reply_to_client
from utils.message import record_message
from loguru import logger


@logger.catch()
def message_service(message: Message):
    if message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "Вышел из обращения к службе поддержки")
        return

    with lock:
        CUR.execute("""SELECT telegram_id FROM users WHERE user_type = '4' """)

    customer = CUR.fetchall()

    data = (message.from_user.id,)
    with lock:
        CUR.execute(""" SELECT phone FROM users WHERE telegram_id = ?""", data)
    phone = CUR.fetchone()[0]

    text = f"<b>Поступило обращение от клиента с номером телефона {phone}\n</b>" \
           f"Текст сообщения:\n" \
           f"<i>{message.text}</i>"
    telegram_id = customer[0]

    # record_message(id_user=message.from_user.id, order="В клиентскую службу",
    #                message_text=message.text, user_type=employee_type)

    for item in telegram_id:
        bot.send_message(item, text, parse_mode='html', reply_markup=reply_to_client.keyboard(message.from_user.id))

    bot.send_message(message.from_user.id,
                     "Ваше сообщение отправлено, ждите пожалуйста обратной связи")

    record_message(id_user=message.from_user.id, order=telegram_id[0],
                   message_text=message.text, user_type='client')


@bot.message_handler(commands=['customer_support'])
def bot_order(message: Message):

    text_message = bot.send_message(message.from_user.id,
                                    "Просьба написать свое обращение.\n"
                                    "Сотрудник клиентского отдела свяжется с вами в ближайшее время\n"
                                    "В случае отказа от обращения, просьба написать 'нет'")

    bot.register_next_step_handler(text_message, message_service)

