import json
import os

from src.utils import (get_exchange_rate, get_greeting, get_stock_price, read_xlsx_file, top_transactions,
                       total_sum_cashback_card)


def get_views(date):
    """
    Главная функция страницы 'Главная', принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    Возвращающую JSON-ответ.
    """
    data_for_json = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(project_root, "course_project_1/data/operations.xlsx")
    transactions = read_xlsx_file(file_path)
    dict_temp = {}
    dict_temp["greeting"] = get_greeting()
    dict_temp["cards"] = total_sum_cashback_card(transactions, date)
    dict_temp["top_transactions"] = top_transactions(transactions, date)
    dict_temp["currency_rates"] = get_exchange_rate()
    dict_temp["stock_prices"] = get_stock_price()
    data_for_json.append(dict_temp)
    return json.dumps(data_for_json, indent=4, ensure_ascii=False)
