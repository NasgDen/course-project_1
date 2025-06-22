import os

from src.reports import spending_by_category
from src.services import get_filter_by_name, get_search, get_search_by_tel, investment_bank
from src.utils import convert_dataframe_to_list, read_xlsx_file
from src.views import get_views

PATH_TO_XLSX_FILE = os.path.join(os.getcwd(), "data", "operations.xlsx")


def main():
    """
    Главная функция
    """
    # Работа функции get_view из модуля view.py
    date_views = input("Введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС: ")
    print(get_views(date_views))

    # Работа функций из модуля service.py
    date_service = input("Введите дату в формате ГГГГ-ММ: ")
    limit = int(input("Введите лимит (10, 50 или 100): "))
    transactions_df = read_xlsx_file(PATH_TO_XLSX_FILE)
    transactions_list = convert_dataframe_to_list(transactions_df)
    print(investment_bank(date_service, transactions_list, limit))
    search_input = input("Введите запрос для поиска в описании или категории: ")
    print(get_search(transactions_list, search_input))
    print(get_filter_by_name(transactions_list))
    print(get_search_by_tel(transactions_list))

    # Работа функций из модуля reports.py
    date_reports = input("Введите дату в формате ДД.ММ.ГГГГ для поиска: ")
    category = input("Введите название категории для поиска: ")
    print(spending_by_category(transactions_df, category, date_reports))


if __name__ == "__main__":
    main()
