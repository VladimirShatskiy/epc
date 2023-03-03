from telebot.types import Message
from loguru import logger
from keyboards import inline
from loader import bot
from config_data.config import TYPE_ORDER
from utils.access_verification import access_verification


@logger.catch
@bot.message_handler(commands=['type'])
@access_verification
def bot_type(message: Message):

    bot.send_message(message.from_user.id, 'Просьба выбрать действие по заказ наряду',
                     reply_markup=inline.order_type.keyboard(TYPE_ORDER))

