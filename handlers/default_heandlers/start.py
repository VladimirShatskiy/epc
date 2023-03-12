from telebot.types import Message
from handlers.custom_handlers import survey
from loader import bot


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
    survey.survey(message)



