import os
import re

from config_data.config import lock, CUR
from handlers.default_heandlers.call_back import callback_query
from loader import bot
from telebot.types import Message, ReplyKeyboardRemove
from handlers.default_heandlers.order import bot_order
import requests
from pyzbar import pyzbar
import cv2

from utils import save_order_to_sql


def barcode_start(message: Message):
    text_message = bot.send_message(message.from_user.id, "Необходимо сделать фотографию штрих кода",
                                    reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(text_message, barcode_return)


def barcode_return(message: Message):
    if message.text:
        bot.send_message(message.from_user.id, "Это не фотография, предлагаю повторить",
                         reply_markup=ReplyKeyboardRemove())
        bot_order(message)

    if message.photo:
        from config_data.config import BOT_TOKEN

        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

    with open("temp.jpg", 'wb') as open_file:
        file = open_file.write(file.content)
    img = cv2.imread("temp.jpg")

    decoded_objects = pyzbar.decode(img)
    if decoded_objects:
        for obj in decoded_objects:
            text = re.findall(r'\d+', string=f'{obj.data}')[0]
            with lock:
                CUR.execute("""SELECT "order" FROM "orders_list" WHERE barcode = ?""", (text,))
                data = CUR.fetchall()
                if data == []:
                    print(f'иду читать папки {text}')
                    temp = save_order_to_sql.list_orders()
                    print(f'вышел из чтения {temp}')
                    with lock:
                        CUR.execute("""SELECT "order" FROM "orders_list" WHERE barcode = ?""", (text,))
                        data = CUR.fetchall()
                    print(f'после прочтения папок {text} {data}')
                    if data == []:
                        print('папки прочитал, все  равно не найден ')
                    else:
                        print("нашелсо второго раза", data[0])
                else:
                    print("Первое чтение когда сразу нашел", data[0])

            bot.send_message(message.from_user.id, text, reply_markup=ReplyKeyboardRemove())
            os.remove("temp.jpg")

    else:
        bot.send_message(message.from_user.id, "Штрих код не распознан, повторите попытку, "
                                               "возможно вы используете изображение с монитора")
        os.remove("temp.jpg")
        bot_order(message)

