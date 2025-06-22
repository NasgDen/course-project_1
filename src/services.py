import json
import re
import os
import logging
from datetime import datetime


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
PATH_TO_LOG_FILE = os.path.join(project_root, "course_project_1/logs/services.log")
services_log = logging.getLogger(__name__)
services_log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_TO_LOG_FILE, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
services_log.addHandler(file_handler)


def investment_bank(month: str, transactions: list[dict], limit: int) -> float:
    """
    Функция принимает список транзакций, порог округления 10, 50 или 100 ₽ и дату. Траты будут округляться,
    и разница между фактической суммой трат по карте и суммой округления будет попадать на счет «Инвесткопилки».
    """
    services_log.info(f"Вызов функции {investment_bank.__name__}")
    date = month
    invest_sum = 0
    if limit == 10 or limit == 50 or limit == 100:
        for transaction in transactions:
            datetime_object = datetime.strptime(str(transaction["Дата операции"]), "%d.%m.%Y %H:%M:%S")
            new_date_string = datetime_object.strftime("%Y-%m")
            if (date == new_date_string and transaction["Сумма операции"] < 0
                    and transaction["Сумма операции"] % limit != 0):
                invest = (limit - (abs(transaction["Сумма операции"]) % limit))
                invest_sum += invest
        services_log.info(f"Успешное выполнение функции {investment_bank.__name__}")
        services_log.debug(f"Значение функции {investment_bank.__name__} : {round(invest_sum, 2)}")
        return round(invest_sum, 2)
    services_log.error(f"Ошибка. Неправильное значение порога округления {investment_bank.__name__}")
    return 0


def get_search(transaction: list[dict], search: str):
    """
    Функция принимает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории.
    """
    services_log.info(f"Вызов функции {get_search.__name__}")
    find = list(filter(lambda d: (search in str(d["Категория"])) or (search in str(d["Описание"])), transaction))
    services_log.info(f"Успешное выполнение функции {get_search.__name__}")
    services_log.debug(f"Значение функции {get_search.__name__} : {json.dumps(find, ensure_ascii=False, indent=4)}")
    return json.dumps(find, ensure_ascii=False, indent=4)


def get_search_by_tel(transaction: list[dict]):
    """
    Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера.
    """
    services_log.info(f"Вызов функции {get_search_by_tel.__name__}")
    pattern = r"\+\d \d{3} \d{3}-\d{2}-\d{2}"
    find = list(filter(lambda d: (re.search(pattern, d["Описание"])), transaction))
    services_log.info(f"Успешное выполнение функции {get_search_by_tel.__name__}")
    services_log.debug(
        f"Значение функции {get_search_by_tel.__name__} : {json.dumps(find, ensure_ascii=False, indent=4)}")
    return json.dumps(find, ensure_ascii=False, indent=4)


def get_filter_by_name(transaction):
    """
    Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам.
    Категория такой транзакции — Переводы, а в описании есть имя и первая буква фамилии с точкой.
    """
    services_log.info(f"Вызов функции {get_filter_by_name.__name__}")
    pattern = r"\b[А-Я]\w+\s[А-Я]\."
    find = list(filter(lambda d: (re.search(pattern, d["Описание"])) and d["Категория"] == "Переводы", transaction))
    services_log.info(f"Успешное выполнение функции {get_filter_by_name.__name__}")
    services_log.debug(
        f"Значение функции {get_filter_by_name.__name__} : {json.dumps(find, ensure_ascii=False, indent=4)}")
    return json.dumps(find, ensure_ascii=False, indent=4)
