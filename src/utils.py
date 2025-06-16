import pandas as pd


def read_xlsx_file(path: str):
    try:
        transactions = pd.read_excel(path)
        return transactions
    except FileNotFoundError:
        return []
