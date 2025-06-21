import datetime
import pandas as pd
from functools import wraps
import json


def json_decorator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(function.__name__)
        result = function(*args, **kwargs)
        df_to_json = result.to_json(orient='records', indent=4)
        print(df_to_json)
        with open(f"{function.__name__}.json", mode="w", encoding="utf-8") as file:
            print(file)
            result.to_json(file, orient='records', indent=4, force_ascii=False)
        return result
    return wrapper

@json_decorator
def spending_by_category(transactions, cateroty: str, data: str=""):
    if data:
        date_start = datetime.datetime.strptime(data, "%d.%m.%Y")
        date_end = date_start - datetime.timedelta(days=90)
        print(type(date_start))
    else:
        date_start = datetime.datetime.now()
        date_end = date_start - datetime.timedelta(days=90)
        print(date_start, date_end)
    return transactions[(transactions["Категория"] == cateroty) &
                        (pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y") < date_start) &
                        (pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y") > date_end)]



