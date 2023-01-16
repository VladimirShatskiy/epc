import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('order', "Выбрать заказ наряд"),
    ('type', "Выбрать действие")
)

BRANCH_USER_DATA = 'user_data'
BRANCH_PHOTO = 'Photo'
BRANCH_ORDER = 'Order'

GlobalOrderDict = {}  # список всех директорий со списками заказ нарядов


TYPE_ORDER = \
    {
        "Прием автомобилей": "Inspection",
        "Текущие рекомендации": "Recommendation",
        "Кузовные повреждения": "BodyDamage",
        "Прочее": "Other"
    }

FILE_CONFIG_START = {
    'order': '',
    'type': '',
    'rus_type': ''
}
