from telebot.types import Message
from config_data.config import CUR, lock
from utils import order
from loader import bot


@bot.message_handler(commands=['order'])
def bot_order(message: Message):
    order.choice(message)



