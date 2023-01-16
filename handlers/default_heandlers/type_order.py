from telebot.types import Message

from keyboards import inline
from loader import bot
from config_data.config import TYPE_ORDER


@bot.message_handler(commands=['type'])
def bot_type(message: Message):
    bot.send_message(message.chat.id, 'Просьба выбрать действие по заказ наряду',
                     reply_markup=inline.order_type.keyboard(TYPE_ORDER))
