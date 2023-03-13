from config_data.config import CUR, lock, ORGANIZATION_NAME, CONNECT_BASE
from handlers.default_heandlers.text import record_message
from loader import bot

global ID_CLIENT


def reply_to(message):
    if message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "Вышел из отправки сообщения")
        return

    global ID_CLIENT

    employee_id = (message.from_user.id,)
    with lock:
        CUR.execute("SELECT 'name', access_level FROM users JOIN access_level \n"
                    "    ON users.user_type = access_level.type_id WHERE telegram_id = ?", employee_id)
    data = CUR.fetchall()
    employee_name, employee_type = data[0][0], data[0][1]

    text = f"<b><i>Сообщение от {employee_name}, {ORGANIZATION_NAME}</i></b>\n" \
           f"{message.text}"
    bot.send_message(ID_CLIENT, text, parse_mode='html')

    data = (message.from_user.id, ID_CLIENT,)
    with lock:
        CUR.execute("""UPDATE users SET to_answer_id = ? WHERE telegram_id = ?""", data)
        CONNECT_BASE.commit()

    record_message(id_user=message.from_user.id, order=ID_CLIENT,
                   message_text=message.text, user_type=employee_type)


def reply(message, id_client):
    global ID_CLIENT

    ID_CLIENT = id_client

    text_message = bot.send_message(message.from_user.id, 'Просьба написать сообщение клиенту или набрать "нет"')
    bot.register_next_step_handler(text_message, reply_to)
