from telebot.types import Message

from botapp.heandlers.default_heandlers.survey import survey
from botapp.keyboards.inline.catalog import product_groups
from botapp.utils.basket import show_order
from botapp.utils.message import message_add_to_sql, message_delete
from botapp.utils.order import get_all_orders
from botapp.utils.seartch import search_product_by_string
from loader import bot
from manage import logger
from shop_bot.settings import MY_DEBUG


@bot.message_handler(commands=['start'])
@logger.catch
def bot_order(message: Message):
    if MY_DEBUG:
        logger.info("начало: @bot.message_handler(commands=['start'])")
    bot.delete_message(message.chat.id, message.message_id)
    message_add_to_sql(
        bot.send_message(message.from_user.id, "Данный бот покажет и закажет для вас товары\n")
    )
    survey(message)

    if MY_DEBUG:
        logger.info("выход @bot.message_handler(commands=['start'])")


@bot.message_handler(commands=['catalog'])
@logger.catch
def bot_order(message: Message):
    if MY_DEBUG:
        logger.info("начало: @bot.message_handler(commands=['catalog'])")

    bot.delete_message(message.chat.id, message.message_id)
    message_delete(message.from_user.id)

    message_add_to_sql(
        bot.send_message(message.from_user.id, text="Выберите группу товаров", reply_markup=product_groups())
    )

    if MY_DEBUG:
        logger.info("выход @bot.message_handler(commands=['catalog'])")


@bot.message_handler(commands=['basket'])
@logger.catch
def bot_order(message: Message):
    if MY_DEBUG:
        logger.info("начало: @bot.message_handler(commands=['basket'])")

    bot.delete_message(message.chat.id, message.message_id)
    message_delete(message.from_user.id)

    show_order(message)

    if MY_DEBUG:
        logger.info("выход @bot.message_handler(commands=['basket'])")


@bot.message_handler(commands=['search'])
@logger.catch
def bot_order(message: Message):
    if MY_DEBUG:
        logger.info("начало: @bot.message_handler(commands=['search'])")

    bot.delete_message(message.chat.id, message.message_id)
    message_delete(message.from_user.id)
    search_product_by_string(message=message)

    if MY_DEBUG:
        logger.info("выход @bot.message_handler(commands=['search'])")


@bot.message_handler(commands=['all_orders'])
@logger.catch
def bot_order(message: Message):
    if MY_DEBUG:
        logger.info("начало: @bot.message_handler(commands=['all_orders'])")

    bot.delete_message(message.chat.id, message.message_id)
    message_delete(message.from_user.id)

    get_all_orders(message)

    if MY_DEBUG:
        logger.info("выход @bot.message_handler(commands=['all_orders'])")

