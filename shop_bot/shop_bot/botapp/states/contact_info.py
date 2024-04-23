from telebot.handler_backends import State, StatesGroup


class UserInfo(StatesGroup):
    name = State()
    age = State()
    phone_number = State()

