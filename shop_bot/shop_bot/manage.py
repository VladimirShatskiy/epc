#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# настройка логирования
from loguru import logger

logger.remove()
logger.add("debug.log", filter=lambda record: record["level"].name == "DEBUG", rotation='1 MB', enqueue=True)
logger.add("info.log", filter=lambda record: record["level"].name == "INFO", rotation='1 MB', enqueue=True)
logger.add("error.log", filter=lambda record: record["level"].name == "ERROR", rotation='1 MB', enqueue=True)
logger.add(sys.stderr, enqueue=True)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_bot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
