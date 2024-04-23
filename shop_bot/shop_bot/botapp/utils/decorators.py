import time
from functools import wraps

from loguru import logger


def timeit(func):
    """
    Декоратор замера скорости выполнения функции
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f'{func.__name__} выполнялась {end - start:.6f} секунд')
        return result

    return wrapper
