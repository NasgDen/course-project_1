import pandas as pd
import datetime


def read_xlsx_file(path: str):
    try:
        transactions = pd.read_excel(path)
        transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
        return transactions
    except FileNotFoundError:
        return []


def convert_dataframe_to_list(transactions_df) -> list[dict]:
    return transactions_df.to_dict("records")


def transactions_filter_by_date(date):
    """
    Функция приведение дат для фильтрования DataFrame transactions
    """
    date_end = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_start = date_end.replace(day=1)
    date_end_filter = (date_end.date()).strftime("%Y-%m-%d")
    date_start_filter = (date_start.date()).strftime("%Y-%m-%d")
    return date_start_filter, date_end_filter