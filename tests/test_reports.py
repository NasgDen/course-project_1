from os import path, remove

import pandas as pd
from pandas.testing import assert_frame_equal

from src.reports import json_decorator, json_decorator_with_filename, spending_by_category


def test_spending_by_category(transactions_df):
    df_func = spending_by_category(transactions_df, "Связь", "10.12.2021")
    assert_frame_equal(df_func, transactions_df)


# Тест декоратора json_decorator_with_filename с записью в файл
@json_decorator_with_filename("log.json")
def devide_file(a, b):
    return pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})


# Тест декоратора json_decorator_with_filename с записью в файл
def test_json_decorator_with_filename():
    result = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    devide_file(10, 5)
    assert path.exists("log.json")
    with open("log.json", mode="r", encoding="utf-8") as file:
        assert file.read() == result.to_json(orient='records', indent=4)
    remove("log.json")


# Тест декоратора json_decorator с записью в файл
@json_decorator
def devide(a, b):
    return pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})


# Тест декоратора json_decorator с записью в файл
def test_decorators_out(capsys):
    devide(10, 5)
    captured = capsys.readouterr()
    assert captured.out == "devide\n"
    remove("devide.json")
