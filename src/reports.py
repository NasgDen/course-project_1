import datetime
import logging
import os
from functools import wraps

import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
PATH_TO_LOG_FILE = os.path.join(project_root, "course_project_1/logs/reports.log")
reports_log = logging.getLogger(__name__)
reports_log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_TO_LOG_FILE, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
reports_log.addHandler(file_handler)


# Декоратор с параметром — принимает имя файла в качестве параметра.
def json_decorator_with_filename(filename):
    def decorator_func(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            with open(filename, mode="w", encoding="utf-8") as file:
                result.to_json(file, orient='records', indent=4, force_ascii=False)
            return result
        return wrapper
    return decorator_func


# Декоратор без параметра — записывает данные отчета в файл с названием по умолчанию
def json_decorator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(function.__name__)
        result = function(*args, **kwargs)
        with open(f"{function.__name__}.json", mode="w", encoding="utf-8") as file:
            result.to_json(file, orient='records', indent=4, force_ascii=False)
        return result
    return wrapper


@json_decorator_with_filename("reports.json")
def spending_by_category(transactions, category: str, data: str = ""):
    """
    Функция принимает на вход: датафрейм с транзакциями, название категории, опциональную дату.
    Если дата не передана, то берется текущая дата.
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    reports_log.info(f"Вызов функции {spending_by_category.__name__}")
    if data:
        reports_log.info(f"Функция {spending_by_category.__name__}: входной аргумент 'дата' задана - {data}")
        date_start = datetime.datetime.strptime(data, "%d.%m.%Y")
        date_end = date_start - datetime.timedelta(days=90)
        print(type(date_start))
    else:
        reports_log.info(f"Функция {spending_by_category.__name__}: входной аргумент 'дата' не задан - {data}")
        date_start = datetime.datetime.now()
        date_end = date_start - datetime.timedelta(days=90)
        print(date_start, date_end)
    reports_log.info(f"Успешное выполнение функции {spending_by_category.__name__}")
    return transactions[(transactions["Категория"] == category) &
                        (pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y") < date_start) &
                        (pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y") > date_end)]
