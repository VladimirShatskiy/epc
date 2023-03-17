from loader import bot
from telebot.types import Message
from handlers.default_heandlers.order import bot_order
import requests
from pyzbar import pyzbar
import cv2


def barcode_start(message: Message):
    text_message = bot.send_message(message.from_user.id, "Необходимо сделать фотографию штрих кода", reply_markup='')
    bot.register_next_step_handler(text_message, barcode_return)


def barcode_return(message: Message):
    if message.text:
        bot.send_message(message.from_user.id, "Это не фотография, предлагаю повторить", reply_markup='')
        bot_order(message)

    if message.photo:
        from config_data.config import BOT_TOKEN

        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

        with open("temp.png", 'wb') as open_file:
            file = open_file.write(file.content)
            # cv2.imshow("img", file)
            print('1')
            img = cv2.imread(file)
            print('2')
            cv2.imshow("img", decode(img))


def decode(image):
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        print(f"Обнаружен штрих-код:\n{obj}")
        image = draw_barcode(obj, image)
        # print barcode type & data
        print("Тип:", obj.type)
        print("Данные:", obj.data)
        print()

    return image


def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    # раскомментируйте выше и закомментируйте ниже, если хотите нарисовать многоугольник, а не прямоугольник
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    return image