import re
import pytesseract
import cv2
from imutils import contours
import requests

from config_data.config import CUR, lock
from handlers.default_heandlers.order import bot_order
from keyboards import inline
from loader import bot
from telebot.types import Message, ReplyKeyboardRemove

from utils.save_order_to_sql import list_orders
from utils import plate_number_form

def reader_plate(cnts, fileimage: object, plate_namders: list, carplate_image_RGB):
    for contur in cnts:
        area = cv2.contourArea(contur)
        x, y, w, h = cv2.boundingRect(contur)

        if area > 5000:
            img = fileimage[y:y+h, x:x+w]
            result = pytesseract.image_to_string(image=img, lang='rus+eng')
            if len(result) > 5:
                databl = re.findall(r'\d{4} \w{2}-\d', result)
                databl_legal_namber = re.findall(r'\w{2} \d{4}-\d', result)
                if databl:
                    plate_namders.append(databl[0])
                    carplate_image_RGB = cv2.rectangle(carplate_image_RGB, (x, y), (x + w, y + h), (0, 255, 0), 2)
                elif databl_legal_namber:
                    databl = databl_legal_namber[0:6] + ' ' + databl_legal_namber[0:1] + '-' + databl_legal_namber[8]
                    plate_namders.append(databl[0])
                    carplate_image_RGB = cv2.rectangle(carplate_image_RGB, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # img = cv2.resize(carplate_image_RGB, (800, 600))
    # cv2.imshow('test', carplate_image_RGB)
    # cv2.waitKey()
    return plate_namders, carplate_image_RGB


def car_plate_number(message):
    if message.text:
        bot.send_message(message.from_user.id, "Это не фотография, предлагаю повторить",
                         reply_markup=ReplyKeyboardRemove())
        bot_order(message)

    if message.photo:
        from config_data.config import BOT_TOKEN

        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

        with open("temp_plate.jpg", 'wb') as open_file:
            open_file.write(file.content)

        carplate_image_RGB = cv2.imread("temp_plate.jpg")
        height, width, _ = carplate_image_RGB.shape
        gray = cv2.cvtColor(carplate_image_RGB, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
        gaus = cv2.GaussianBlur(thresh, (5, 5), 0)
        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts, _ = contours.sort_contours(cnts[0])

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        plate_namders = []

        plate_namders, carplate_image_RGB\
            = reader_plate(cnts=cnts, fileimage=gray, carplate_image_RGB=carplate_image_RGB, plate_namders=plate_namders)

        if not plate_namders:
            plate_namders, carplate_image_RGB \
                = reader_plate(cnts=cnts, fileimage=gaus, carplate_image_RGB=carplate_image_RGB,
                               plate_namders=plate_namders)
            if not plate_namders:
                text = "Номер не распознан, попробуйте сделать фотографию повторно"
                bot.send_message(message.from_user.id, text)
                bot_order(message)
                return
            else:
                text = (plate_namders[0])
        else:
            text = (plate_namders[0])
        txt = f'Распознал гос номер {text}, ищу отрытые заказ наряды'
        bot.send_message(message.from_user.id, txt)

        # Проверяю заказ наряды в базе
        # Обновляю Базу по всем папкам
        list_orders()
        data = (plate_number_form.read(text),)

        with lock:
            CUR.execute("""SELECT "order" FROM orders_list 
            WHERE plate_number = ? AND closed = FALSE""", data)
        read_data = CUR.fetchall()
        lo = []
        for item in read_data:
            lo.append(item[0])
        if not read_data:
            bot.send_message(message.from_user.id, "Открытые заказ наряды соответствующие номеру не найдены")
            bot_order(message)
        else:
            bot.send_message(message.from_user.id, "Просьба выбрать заказ наряд",
                             reply_markup=inline.choice_order.keyboard(lo))


def get_plate_number_start(message: Message):
    text_message = bot.send_message(message.from_user.id, "Необходимо сделать автомобиля с гос номером",
                                    reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(text_message, car_plate_number)
