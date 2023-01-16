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
    ('order', "Выбрать заказ наряд")
)

BRANCH_USER_DATA = 'user_data'
BRANCH_PHOTO = 'Photo'
BRANCH_ORDER = 'Order'

GlobalOrderDict = {}  # список всех директорий со списками заказ нарядов
GlobalOrder = ''  # номер заказ наряда для выгрузки фото
GlobalItem = ''  # выбор критерия сохранения фото (осмотр/неисправность/кузовное повреждение)

TYPE_ORDER = \
    {
        "Прием автомобилей": "Inspection",
        "Текущие рекомендации": "Recommendation",
        "Кузовные повреждения": "BodyDamage",
        "Прочее": "Other"
    }
