import os
from telebot.types import Message
import json
from config_data.config import FILE_CONFIG_START, BRANCH_USER_DATA


def create_user_file(message: Message) -> None:
    """
    Создание файлов конфигурации для пользователей
    """

    file_config = str(message.from_user.id) + '_conf.txt'

    if not os.path.exists(BRANCH_USER_DATA):
        os.mkdir(BRANCH_USER_DATA)

    with open(os.path.join(BRANCH_USER_DATA, file_config), 'w', encoding='utf-8') as file:
        json.dump(FILE_CONFIG_START, file, indent=4)

