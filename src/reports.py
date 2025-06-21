import datetime
import pandas as pd
from functools import wraps

def json_decorator_with_filename(filename):
    def decorator_func(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            print(function.__name__)
            result = function(*args, **kwargs)
            with open(filename, mode="w", encoding="utf-8") as file:
                print(file)
                result.to_json(file, orient='records', indent=4, force_ascii=False)
            return result
        return wrapper
    return decorator_func


def json_decorator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(function.__name__)
        result = function(*args, **kwargs)
        with open(f"{function.__name__}.json", mode="w", encoding="utf-8") as file:
            print(file)
            result.to_json(file, orient='records', indent=4, force_ascii=False)
        return result
    return wrapper

@json_decorator_with_filename("reports.json")
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



