from loguru import logger
from telebot.types import Message
from loader import bot



# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
@logger.catch
def bot_echo(message: Message):

    bot.reply_to(message, "Пока не решил как ответить на \nСообщение:"
                          f"{message.text}")

