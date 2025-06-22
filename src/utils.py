import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
PATH_TO_LOG_FILE = os.path.join(project_root, "course_project_1/logs/utils.log")
utils_log = logging.getLogger(__name__)
utils_log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_TO_LOG_FILE, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_log.addHandler(file_handler)


def read_xlsx_file(path: str):
    """
    Функция чтение EXCEL файла
    """
    utils_log.info(f"Вызов функции {read_xlsx_file.__name__}")
    try:
        transactions = pd.read_excel(path)
        utils_log.info(f"Успешное чтение файла {path}")
        return transactions
    except FileNotFoundError:
        utils_log.error(f"Файл {path} не найден")
        return []


def convert_dataframe_to_list(transactions_df) -> list[dict]:
    """
    Функция конвертирует тип DataFrame в Список словарей(list[dict])
    """
    utils_log.info(f"Вызов функции {convert_dataframe_to_list.__name__}")
    return transactions_df.to_dict("records")


def transactions_filter_by_date(date):
    """
    Функция приведение дат для фильтрования DataFrame transactions
    """
    utils_log.info(f"Вызов функции {transactions_filter_by_date.__name__}")
    date_end = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_start = date_end.replace(day=1)
    date_end_filter = (date_end.date()).strftime("%Y-%m-%d")
    date_start_filter = (date_start.date()).strftime("%Y-%m-%d")
    utils_log.info(f"Успешное выполнение функции {transactions_filter_by_date.__name__}")
    utils_log.debug(f"Значение функции {transactions_filter_by_date.__name__} : {date_start_filter, date_end_filter}")
    return date_start_filter, date_end_filter


def get_greeting() -> str:
    """
    Функция возвращает приветствие - «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени суток.
    """
    utils_log.info(f"Вызов функции {get_greeting.__name__}")
    date_time_now = datetime.datetime.now()
    hour_now = date_time_now.hour
    if 0 <= hour_now < 6:
        utils_log.debug(f"Функции {get_greeting.__name__} возвратило значение - Доброй ночи")
        return "Доброй ночи"
    elif 6 <= hour_now < 12:
        utils_log.debug(f"Функции {get_greeting.__name__} возвратило значение - Доброе утро")
        return "Доброе утро"
    elif 12 <= hour_now < 18:
        utils_log.debug(f"Функции {get_greeting.__name__} возвратило значение - Добрый день")
        return "Добрый день"
    else:
        utils_log.debug(f"Функции {get_greeting.__name__} возвратило значение - Добрый вечер")
        return "Добрый вечер"


def total_sum_cashback_card(transactions, date: str) -> list[dict]:
    """
    Функция принимает DataFrame c транзакциями и выводит по каждой карте:
    последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые 100 рублей).
    """
    utils_log.info(f"Вызов функции {total_sum_cashback_card.__name__}")
    cards_info = []
    date_filter = transactions_filter_by_date(date)
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
    # Фильтрование DataFrame transactions по диапазону дат и группировка по "номеру карты"
    try:
        transactions_filtered = transactions[transactions["Дата платежа"].between(date_filter[0], date_filter[1])]
        cards_group = transactions_filtered.groupby("Номер карты")
        total_sum = abs(
            cards_group.apply(lambda x: x[x["Сумма операции"] < 0]["Сумма операции"].sum(), include_groups=False)
        )
        total_sum_dict = total_sum.to_dict()
        # Формирование списка словарей для вывода
        for key, value in total_sum_dict.items():
            cards_temp = {}
            cards_temp["last_digits"] = key[1:]
            cards_temp["total_spent"] = round(value, 2)
            cards_temp["cashback"] = round(cards_temp["total_spent"], 2) * 0.01
            cards_info.append(cards_temp)
        utils_log.info(f"Успешное выполнение функции {total_sum_cashback_card.__name__}")
        utils_log.debug(f"Значение функции {total_sum_cashback_card.__name__} : {cards_info}")
        return cards_info
    except Exception as err:
        utils_log.info(f"Функция {total_sum_cashback_card.__name__} Введенной даты нет в транзакциях")
        return []
    # if transactions_filtered.index:
    #     print("индекс")
    # else:
    #     print("Нет индекса")
    # print(transactions_filtered.iloc[0])



def top_transactions(transactions, date):
    """
    Функция принимает DataFrame c транзакциями и Топ-5 транзакций по сумме платежа.:
    """
    utils_log.info(f"Вызов функции {top_transactions.__name__}")
    top_trans = []
    date_filter = transactions_filter_by_date(date)
    # Фильтрование DataFrame transactions по диапазону дат и группировка по "номеру карты"
    transactions_filtered = transactions[transactions["Дата платежа"].between(date_filter[0], date_filter[1])]
    sorted_trans_by_sum = transactions_filtered.sort_values(by="Сумма платежа", ascending=True)
    sorted_trans_temp = sorted_trans_by_sum.head(5).to_dict("records")
    for trans in sorted_trans_temp:
        temp_dict = {}
        temp_dict["date"] = trans.get("Дата операции")
        temp_dict["amount"] = trans.get("Сумма операции с округлением")
        temp_dict["category"] = trans.get("Категория")
        temp_dict["description"] = trans.get("Описание")
        top_trans.append(temp_dict)
    utils_log.info(f"Успешное выполнение функции {top_transactions.__name__}")
    utils_log.debug(f"Значение функции {top_transactions.__name__} : {top_trans}")
    return top_trans


def get_stock_price() -> list[dict] | str:
    """
    Функция подключается внешнему API - www.alphavantage.co и возвращает стоимость акций из S&P500:
    "AAPL", "AMZN", "GOOGL", "MSFT","TSLA"
    """
    utils_log.info(f"Вызов функции {get_stock_price.__name__}")
    path_env = os.path.join(os.getcwd(), ".env")
    load_dotenv(path_env)
    api_key = os.getenv("API_KEY")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(project_root, "course_project_1/user_settings.json")
    with open(file_path, mode="r", encoding="utf-8") as file:
        stock_names = json.load(file)
    stock_prices = []

    for name in stock_names["user_stocks"]:
        stock_dict = {}
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={name}&apikey={api_key}"
        try:
            req_url = requests.get(url)
            utils_log.info(f"Функция {get_stock_price.__name__}: Успешное подключение к API - alphavantage.co")
        except requests.exceptions.ConnectionError:
            utils_log.error(f"Функция {get_stock_price.__name__}: Ошибка подключения. Проверьте сетевое подключение.")
            return "Ошибка подключения. Проверьте сетевое подключение."
        data = req_url.json()
        date = (data.get("Meta Data", {})).get("3. Last Refreshed")
        name_stock = (data.get("Meta Data", {})).get("2. Symbol")
        price_stock = ((data.get("Time Series (Daily)", {})).get(date, {})).get("4. close", {})
        stock_dict["stock"] = name_stock
        stock_dict["price"] = price_stock
        stock_prices.append(stock_dict)
    utils_log.info(f"Успешное выполнение функции {get_stock_price.__name__}")
    utils_log.debug(f"Значение функции {get_stock_price.__name__} : {stock_prices}")
    return stock_prices


def get_exchange_rate():
    """
    Функция подключается внешнему API - www.apilayer.com и возвращает курсы валют.
    """
    utils_log.info(f"Вызов функции {get_exchange_rate.__name__}")
    exchange = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(project_root, "course_project_1/user_settings.json")
    with open(file_path, mode="r", encoding="utf-8") as file:
        currency = json.load(file)
    path_env = os.path.join(os.getcwd(), ".env")
    load_dotenv(path_env)
    api_key = os.getenv("API_KEY_EXCHANGE")
    payload = {}
    headers = {"apikey": f"{api_key}"}
    for name in currency["user_currencies"]:
        exchange_dict = {}
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={name}&amount=1"
        try:
            response = requests.get(url, headers=headers, data=payload)
            utils_log.info(f"Функция {get_exchange_rate.__name__}: Успешное подключение к API - api.apilayer.com")
        except requests.exceptions.ConnectionError:
            utils_log.error(f"Функция {get_exchange_rate.__name__}:Ошибка подключения. Проверьте сетевое подключение")
            return "Ошибка подключения. Проверьте сетевое подключение."
        result = response.json()
        exchange_dict["currency"] = name
        exchange_dict["rate"] = result.get("result")
        exchange.append(exchange_dict)
    utils_log.info(f"Успешное выполнение функции {get_exchange_rate.__name__}")
    utils_log.debug(f"Значение функции {get_exchange_rate.__name__} : {exchange}")
    return exchange
