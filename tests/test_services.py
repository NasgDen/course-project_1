from src.services import investment_bank


# Тест функции investment_bank
def test_investment_bank(top_transactions_list):
    assert investment_bank("2021-12", top_transactions_list, 10) == 14.2


# Тест функции investment_bank пустой список
def test_investment_bank_zero(top_transactions_list):
    assert investment_bank("2021-12", [], 10) == 0


# Тест функции investment_bank пустая дата
def test_investment_bank_not_date(top_transactions_list):
    assert investment_bank("", top_transactions_list, 10) == 0


