import os

from src.services import investment_bank
from src.utils import convert_dataframe_to_list, read_xlsx_file
from src.views import get_exchange_rate, get_stock_price, top_transactions, total_sum_cashback_card

PATH_TO_XLSX_FILE = os.path.join(os.getcwd(), "data", "operations.xlsx")
# PATH_TO_JSON_FILE = os.path.join(os.getcwd(), "data", "views.json")


def main():
    transactions_df = read_xlsx_file(PATH_TO_XLSX_FILE)
    print(total_sum_cashback_card(transactions_df, "2021-12-2 00:00:00"))
    # print(top_transactions(transactions_df))
    # print(get_stock_price())
    # print(get_exchange_rate())
    transactions = convert_dataframe_to_list(transactions_df)
    # date = input("Введите дату в формате ГГГГ-ММ: ")
    # limit = int(input("Введите лимит (10, 50 или 100): "))
    # print(investment_bank(date, transactions, limit))


if __name__ == "__main__":
    main()
