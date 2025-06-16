import os

from src.utils import read_xlsx_file
from src.views import top_transactions, total_sum_cashback_card

PATH_TO_XLSX_FILE = os.path.join(os.getcwd(), "data", "operations.xlsx")


def main():
    transactions = read_xlsx_file(PATH_TO_XLSX_FILE)
    print(total_sum_cashback_card(transactions))
    print(top_transactions(transactions))


if __name__ == "__main__":
    main()
