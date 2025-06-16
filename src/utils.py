import pandas as pd


def read_xlsx_file(path):
    try:
        transactions = pd.read_excel(path)
        return transactions.to_dict("records")
    except FileNotFoundError:
        return []

