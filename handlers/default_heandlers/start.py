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

    bot.reply_to(message, f"Добрый день, {message.from_user.full_name}!\n"
                          f"Этот бот помогает клиентам следить за состоянием своего автомобиля "
                          f"находясь вне сервисной станции\n"
                          f"Сюда будут поступать все фото и видео материалы по обслуживанию автомобиля\n"
                          f"Так же, в меню доступна связь со службой помощи клиентам\n"
                          f"Если даже Вы уже забрали свой автомобиль всегда всегда можно оставить "
                          f"комментарии и мы с Вами обязательно свяжемся и ответим на возникшие вопросы"
                 )
    survey.survey(message)



