from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    text = '\n'.join(text) + "\n\nБот предназначен для загрузки фотографий/видео и файлов необходимых для истории " \
                             "проведения ремонтов автомобилей\n"
    bot.reply_to(message, text)
