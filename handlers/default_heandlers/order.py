from telebot.types import Message
from utils import order
from loader import bot


@bot.message_handler(commands=['order'])
def bot_help(message: Message):
    order.choice(message)