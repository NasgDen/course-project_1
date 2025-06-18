import datetime
import os

import requests
from dotenv import load_dotenv


def get_greeting() -> str:
    """
    Функция возвращает приветствие - «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени суток.
    """
    date_time_now = datetime.datetime.now()
    hour_now = date_time_now.hour
    if 0 <= hour_now < 6:
        return "Доброй ночи"
    elif 6 <= hour_now < 12:
        return "Доброе утро"
    elif 12 <= hour_now < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def total_sum_cashback_card(transactions) -> list[dict]:
    """
    Функция принимает DataFrame c транзакциями и выводит по каждой карте:
    последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые 100 рублей).
    """
    cards_info = []
    cards_group = transactions.groupby("Номер карты")
    total_sum = abs(cards_group.apply(lambda x: x[x["Сумма операции"] < 0]
                    ["Сумма операции"].sum(), include_groups=False))
    total_sum_dict = total_sum.to_dict()
    for key, value in total_sum_dict.items():
        cards_temp = {}
        cards_temp["last_digits"] = key[1:]
        cards_temp["total_spent"] = round(value, 2)
        cards_temp["cashback"] = round(cards_temp["total_spent"], 2) * 0.01
        cards_info.append(cards_temp)
    return cards_info


def top_transactions(transactions):
    """
    Функция принимает DataFrame c транзакциями и Топ-5 транзакций по сумме платежа.:
    """
    top_trans = []
    sorted_trans_by_sum = transactions.sort_values(by="Сумма платежа", ascending=True)
    sorted_trans_temp = sorted_trans_by_sum.head(5).to_dict("records")
    for trans in sorted_trans_temp:
        temp_dict = {}
        temp_dict["date"] = trans.get("Дата операции")
        temp_dict["amount"] = trans.get("Сумма операции с округлением")
        temp_dict["category"] = trans.get("Категория")
        temp_dict["description"] = trans.get("Описание")
        top_trans.append(temp_dict)
    return top_trans


def get_stock_price() -> list[dict]:
    """
    Функция подключается внешнему API - www.alphavantage.co и возвращает стоимость акций из S&P500:
    "AAPL", "AMZN", "GOOGL", "MSFT","TSLA"
    """
    path_env = os.path.join(os.getcwd(), ".env")
    load_dotenv(path_env)
    api_key = os.getenv("API_KEY")
    stock_names = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    stock_prices = []

    for name in stock_names:
        stock_dict = {}
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={name}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()
        date = data['Meta Data']["3. Last Refreshed"]
        name_stock = data['Meta Data']['2. Symbol']
        price_stock = data["Time Series (Daily)"][date]["4. close"]
        stock_dict["stock"] = name_stock
        stock_dict["price"] = price_stock
        stock_prices.append(stock_dict)
    return stock_prices


def get_exchange_rate():
    """
    Функция подключается внешнему API - www.apilayer.com и возвращает курсы валют.
    """
    exchange = []
    currency = ["USD", "EUR"]
    path_env = os.path.join(os.getcwd(), ".env")
    load_dotenv(path_env)
    api_key = os.getenv("API_KEY_EXCHANGE")
    payload = {}
    headers = {
        "apikey": f"{api_key}"
    }
    for name in currency:
        exchange_dict = {}
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={name}&amount=1"
        try:
            response = requests.get(url, headers=headers, data=payload)
        except requests.exceptions.ConnectionError:
            return "Ошибка подключения. Проверьте сетевое подключение."
        result = response.json()
        exchange_dict["currency"] = name
        exchange_dict["rate"] = round(result.get("result"), 2)
        exchange.append(exchange_dict)
    return exchange
