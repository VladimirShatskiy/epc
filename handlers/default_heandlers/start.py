from os import link

from telebot.types import Message
from loader import bot
from utils import creat_user_base


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Запуск бота
    И подготовка файлов конфигурации

    :return: None
    """

    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\nЭтот бот предназначен для загрузки фотографий/видео"
                          f" и файлов необходимых для истории проведения ремонтов автомобилей\n"
                          f"Для клиентов\n"
                          f"Тут будут загружены все фотографии сделанные сотрудниками сервисного центра по состоянию "
                          f"Вашего автомобиля, в том числе для согласования работ и предложенных рекомендаций\n"
                 )
    creat_user_base.create_user_base(message)



