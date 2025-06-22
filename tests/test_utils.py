import datetime
from unittest.mock import MagicMock, patch

import pandas as pd

from src.utils import (
    get_exchange_rate,
    get_greeting,
    get_stock_price,
    read_xlsx_file,
    top_transactions,
    total_sum_cashback_card,
)


# Тест функции read_excel_file - отсутствие файла
@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_read_excel_file_not_found(mock_read_xls):
    assert read_xlsx_file("test.xls") == []
    mock_read_xls.assert_called_once_with("test.xls")


# Тест функции read_excel_file - корректные данные
@patch("pandas.read_excel")
def test_process_excel_data(mock_read_excel):
    mock_df = pd.DataFrame({"ColumnA": [10, 20, 30], "ColumnB": ["X", "Y", "Z"]})
    mock_read_excel.return_value = mock_df
    read_xlsx_file("dummy_path.xlsx")


# Тест функции get_greeting
def test_get_greeting_day():
    mock_time = datetime.datetime(2025, 6, 21, 13, 0, 0)
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_time
        result = get_greeting()
        assert result == "Добрый день"


def test_get_greeting_evening():
    mock_time = datetime.datetime(2025, 6, 21, 20, 0, 0)
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_time
        result = get_greeting()
        assert result == "Добрый вечер"


def test_get_greeting_night():
    mock_time = datetime.datetime(2025, 6, 21, 2, 0, 0)
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_time
        result = get_greeting()
        assert result == "Доброй ночи"


def test_get_greeting_morning():
    mock_time = datetime.datetime(2025, 6, 21, 10, 0, 0)
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_time
        result = get_greeting()
        assert result == "Доброе утро"


# total_sum_cashback_card
def test_total_sum_cashback_card():
    mock_total_sum_cashback_card = MagicMock(
        return_value=[{"col1": 1, "col2": 4}, {"col1": 2, "col2": 5}, {"col1": 3, "col2": 6}]
    )
    total_sum_cashback_card = mock_total_sum_cashback_card
    assert total_sum_cashback_card() == [{"col1": 1, "col2": 4}, {"col1": 2, "col2": 5}, {"col1": 3, "col2": 6}]


def test_total_sum_cashback_card_valid(transactions_df):
    result = [{"cashback": 0.15, "last_digits": "7197", "total_spent": 15.0}]
    assert total_sum_cashback_card(transactions_df, "2021-12-2 00:00:00") == result


def test_top_transactions(top_transactions_df):
    result = []
    assert top_transactions(top_transactions_df, "2021-12-20 00:00:00") == result


@patch("requests.get")
def test_get_stock_price(mock_get):
    mock_get.return_value.json.return_value = {
        "Meta Data": {"2. Symbol": "AAPL", "3. Last Refreshed": "2025-06-20"},
        "Time Series (Daily)": {
            "2025-06-20": {"1. open": "198.2350", "2. high": "201.7000", "3. low": "196.8550", "4. close": "201.0000"}
        },
    }
    assert get_stock_price() == [
        {"price": "201.0000", "stock": "AAPL"},
        {"price": "201.0000", "stock": "AAPL"},
        {"price": "201.0000", "stock": "AAPL"},
        {"price": "201.0000", "stock": "AAPL"},
        {"price": "201.0000", "stock": "AAPL"},
    ]


@patch("requests.get")
def test_get_exchange_rate(mock_get):
    mock_get.return_value.json.return_value = {"result": 1}
    assert get_exchange_rate() == [{"currency": "USD", "rate": 1}, {"currency": "EUR", "rate": 1}]
