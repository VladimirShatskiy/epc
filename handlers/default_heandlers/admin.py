from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS, CUR
from loader import bot


@bot.message_handler(commands=['admin'])
def bot_admin(message: Message):
    # text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    # text = '\n'.join(text) + "\n\nБот предназначен для загрузки фотографий/видео и файлов необходимых для истории " \
    #                          "проведения ремонтов автомобилей\n" \
    #                          "Данные можно отправлять после выбора заказ наряда и типа действия из меню\n" \
    #                          "Изменить заказ наряд и тип действия можно там же через меню"
    # bot.send_message(message, 'Админка для присвоения статусов клиентам')
    data = (message.from_user.id,)
    CUR.execute("""SELECT access_level FROM users JOIN access_level 
    ON users.user_type = access_level.type_id WHERE telegram_id = ?""", data)

    if CUR.fetchone()[0] != "admin":
        bot.send_message(message.from_user.id, "У Вас нет доступа к данной функции")
        return

    bot.send_message(message.from_user.id, "Доступ админа разрешен")


