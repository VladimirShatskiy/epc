from loader import bot
from utils.get_plate_number import car_plate_number
from utils.save_order_to_sql import list_orders
from utils.set_bot_commands import set_default_commands
import handlers
from loguru import logger
from telebot.custom_filters import StateFilter

logger.add("debug.txt", format="{time} {level} {message}", level="DEBUG", rotation="100 KB")

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()

