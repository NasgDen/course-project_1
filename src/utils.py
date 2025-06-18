import pandas as pd


def read_xlsx_file(path: str):
    try:
        transactions = pd.read_excel(path)
        transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
        return transactions
    except FileNotFoundError:
        return []


def convert_dataframe_to_list(transactions_df) -> list[dict]:
    return transactions_df.to_dict("records")
