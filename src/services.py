from datetime import datetime


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
