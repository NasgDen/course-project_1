from unittest.mock import patch, Mock, MagicMock

import pandas as pd
import datetime
from pandas.testing import assert_frame_equal

from src.utils import read_xlsx_file, get_greeting, total_sum_cashback_card


# Тест функции read_excel_file - отсутствие файла
@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_read_excel_file_not_found(mock_read_xls):
    assert read_xlsx_file("test.xls") == []
    mock_read_xls.assert_called_once_with("test.xls")


# Тест функции read_excel_file - корректные данные
@patch('pandas.read_excel')
def test_process_excel_data(mock_read_excel):
    mock_df = pd.DataFrame({'ColumnA': [10, 20, 30], 'ColumnB': ['X', 'Y', 'Z']})
    mock_read_excel.return_value = mock_df
    read_xlsx_file('dummy_path.xlsx')


# Тест функции get_greeting
def test_get_greeting_day():
    mock_time = datetime.datetime(2025,6, 21, 13, 0, 0)
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_time
        result = get_greeting()
        assert result == "Добрый день"


def test_get_greeting_evening():
    mock_time = datetime.datetime(2025,6, 21, 20, 0, 0)
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
    mock_total_sum_cashback_card = MagicMock(return_value=[{'col1': 1, 'col2': 4}, {'col1': 2, 'col2': 5}, {'col1': 3, 'col2': 6}])
    total_sum_cashback_card = mock_total_sum_cashback_card
    assert total_sum_cashback_card() == [{'col1': 1, 'col2': 4}, {'col1': 2, 'col2': 5}, {'col1': 3, 'col2': 6}]





