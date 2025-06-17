import os

from src.utils import read_xlsx_file
from src.views import get_stock_price, top_transactions, total_sum_cashback_card

PATH_TO_XLSX_FILE = os.path.join(os.getcwd(), "data", "operations.xlsx")
# PATH_TO_JSON_FILE = os.path.join(os.getcwd(), "data", "views.json")


def main():
    transactions = read_xlsx_file(PATH_TO_XLSX_FILE)
    print(total_sum_cashback_card(transactions))
    print(top_transactions(transactions))
    print(get_stock_price())


if __name__ == "__main__":
    main()
