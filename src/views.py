import datetime


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
