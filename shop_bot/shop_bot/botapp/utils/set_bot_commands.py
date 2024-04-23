from telebot.types import BotCommand
from botapp.config_data.config import DEFAULT_COMMANDS

from manage import logger


@logger.catch()
def set_default_commands(bot, commands: list = DEFAULT_COMMANDS) -> None:
    """
    Создание меню бота
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in commands]
    )
