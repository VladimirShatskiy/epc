import os
import sqlite3
import threading

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

CONNECT_BASE = sqlite3.connect('drive.sqlite', check_same_thread=False)
CUR = CONNECT_BASE.cursor()

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('order', "Выбрать заказ наряд"),
    ('type', "Выбрать действие"),
    ('admin', "Администрирование"),
)

lock = threading.Lock()

BRANCH_USER_DATA = 'user_data'
BRANCH_PHOTO = 'Photo'
BRANCH_ORDER = 'Order'
GROUP_ID = ""

GlobalOrderDict = {}  # список всех директорий со списками заказ нарядов

TYPE_ORDER = \
    {
        "Прием автомобилей": "Inspection",
        "Текущие рекомендации": "Recommendation",
        "Кузовные повреждения": "BodyDamage",
        "Прочее": "Other",
        "Для сервисных нужд": "Service"
    }

LENGTH_CLOSED_ORDER = 6  # длина слова закрытого заказ наряда
CLOSED_ORDER = 'closed'  # приписка к заказ наряду показывающие закрытый зн

FILE_CONFIG_START = {
    'order': '',
    'type': '',
    'rus_type': ''
}
