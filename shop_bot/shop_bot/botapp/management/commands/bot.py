
from django.core.management.base import BaseCommand
from telebot.custom_filters import StateFilter

from loader import bot
from botapp.utils.set_bot_commands import set_default_commands

import botapp.heandlers.default_heandlers.commands
import botapp.heandlers.default_heandlers.text
import botapp.heandlers.default_heandlers.call_back
import botapp.heandlers.default_heandlers.photo


class Command(BaseCommand):
    help = 'Запуск telegram бота'

    def handle(self, *args, **kwargs) -> None:

        bot.add_custom_filter(StateFilter(bot))
        set_default_commands(bot)
        bot.infinity_polling(none_stop=True, interval=1)
