from loader import bot
from utils.set_bot_commands import set_default_commands
import handlers
from loguru import logger


logger.add("debug.txt", format="{time} {level} {message}", level="DEBUG", rotation="100 KB")
# logger.debug("Ошибка")
# logger.error("Ошибка")
# # logger.info("Ошибка")

if __name__ == '__main__':
    set_default_commands(bot)
    bot.infinity_polling()
