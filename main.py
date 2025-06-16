import os

from src.utils import read_xlsx_file


PATH_TO_XLSX_FILE = os.path.join(os.getcwd(), "data", "operations.xlsx")
def main():
    transactions = read_xlsx_file(PATH_TO_XLSX_FILE)
    print(transactions)


if __name__ == "__main__":
    main()
