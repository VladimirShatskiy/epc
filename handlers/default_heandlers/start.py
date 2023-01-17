from telebot.types import Message
from loader import bot
from utils.creat_user_file import create_user_file


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Запуск бота
    И подготовка файлов конфигурации

    :return: None
    """
    create_user_file(message)
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\nЭтот бот предназначен для загрузки фотографий/видео"
                          f" и файлов необходимых для истории проведения ремонтов автомобилей\n"
                          f"Данные можно отправлять после выбора заказ наряда и типа действия из меню\n"
                          f"Изменить заказ наряд и тип действия можно там же через меню")


