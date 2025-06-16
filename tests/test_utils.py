from unittest.mock import patch

import pandas as pd

from src.utils import read_xlsx_file


# Тест функции read_excel_file - отсутствие файла
@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_read_excel_file_not_found(mock_read_xls):
    assert read_xlsx_file("test.xls") == []
    mock_read_xls.assert_called_once_with("test.xls")


# Тест функции read_excel_file - корректные данные
@patch("pandas.read_excel")
def test_read_excel_file(mock_read_xls):
    mock_read_xls.return_value = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
    assert read_xlsx_file("test.xls") == [{'col1': 1, 'col2': 4}, {'col1': 2, 'col2': 5}, {'col1': 3, 'col2': 6}]
    mock_read_xls.assert_called_once_with("test.xls")