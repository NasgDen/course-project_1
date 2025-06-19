from datetime import datetime
import json
import re


def investment_bank(month: str, transactions: list[dict], limit: int) -> float:
    """
    Функция принимает список транзакций, порог округления 10, 50 или 100 ₽ и дату. Траты будут округляться,
    и разница между фактической суммой трат по карте и суммой округления будет попадать на счет «Инвесткопилки».
    """
    date = month
    invest_sum = 0
    if limit == 10 or limit == 50 or limit == 100:
        for transaction in transactions:
            datetime_object = datetime.strptime(str(transaction["Дата операции"]), "%d.%m.%Y %H:%M:%S")
            new_date_string = datetime_object.strftime("%Y-%m")
            if (date == new_date_string and transaction["Сумма операции"] < 0
                    and transaction["Сумма операции"] % limit != 0):
                invest = (limit - (abs(transaction["Сумма операции"]) % limit))
                invest_sum += invest
        return round(invest_sum, 2)
    return 0


def get_search(transaction: list[dict], search: str):
    """
    Функция принимает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории.
    """
    find = list(filter(lambda d: (search in str(d["Категория"])) or (search in str(d["Описание"])), transaction))
    return json.dumps(find, ensure_ascii=False, indent=4)


def get_search_by_tel(transaction: list[dict], search: str):
    """
    Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера.
    """
    pattern = r"[\D]"
    replacement = ""
    formatted_search = re.sub(pattern, replacement, search)
    find = list(filter(lambda d: (formatted_search == re.sub(pattern, replacement, d["Описание"])), transaction))
    return json.dumps(find, ensure_ascii=False, indent=4)


def get_filter_by_name(transaction):
    """
    Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам.
    Категория такой транзакции — Переводы, а в описании есть имя и первая буква фамилии с точкой.
    """
    pattern = r"\b[А-Я]\w+\s[А-Я]\."
    find = list(filter(lambda d: (re.search(pattern, d["Описание"])) and d["Категория"] == "Переводы", transaction))
    # with open("filter_by_name.json", mode="w", encoding="utf-8") as file:
    #     json.dump(find, file, ensure_ascii=False, indent=4)
    return json.dumps(find, ensure_ascii=False, indent=4)