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
lock = threading.Lock()


DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('order', "Выбрать заказ наряд"),
    ('type', "Выбрать действие"),
    ('admin', "Администрирование"),
)

ORGANIZATION_NAME = "Драйв Моторс"
BRANCH_PHOTO = 'Photo'

GlobalOrderDict = {}  # список всех директорий со списками заказ нарядов

TYPE_ORDER = \
    {
        "Прием автомобилей": "Inspection",
        "Текущие рекомендации": "Recommendation",
        "Кузовные повреждения": "BodyDamage",
        "Прочее": "Other",
        "Для сервисных нужд": "Service"
    }


CLOSED_ORDER = 'closed'  # приписка к заказ наряду показывающие закрытый зн
LENGTH_CLOSED_ORDER = int(len(CLOSED_ORDER))  # длина слова закрытого заказ наряда




