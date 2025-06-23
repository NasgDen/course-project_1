import json

from src.views import get_views


def test_views():
    result = [
        {
            "greeting": "Добрый вечер",
            "cards": [
                {"last_digits": "4556", "total_spent": 300.0, "cashback": 3.0},
                {"last_digits": "5091", "total_spent": 5711.87, "cashback": 57.1187},
                {"last_digits": "7197", "total_spent": 1033.73, "cashback": 10.3373},
            ],
            "top_transactions": [
                {"date": "02.12.2021 16:26:02", "amount": 5510.8, "category": "Каршеринг", "description": "Ситидрайв"},
                {"date": "02.12.2021 15:18:26", "amount": 496.51, "category": "Супермаркеты", "description": "Магнит"},
                {
                    "date": "29.11.2021 14:40:46",
                    "amount": 300.0,
                    "category": "Местный транспорт",
                    "description": "Метро Санкт-Петербург",
                },
                {
                    "date": "29.11.2021 19:48:21",
                    "amount": 200.0,
                    "category": "Местный транспорт",
                    "description": "Метро Санкт-Петербург",
                },
                {
                    "date": "01.12.2021 13:12:18",
                    "amount": 199.0,
                    "category": "Дом и ремонт",
                    "description": "Строитель",
                },
            ],
            "currency_rates": [{"currency": "USD", "rate": None}, {"currency": "EUR", "rate": None}],
            "stock_prices": [
                {"stock": None, "price": {}},
                {"stock": None, "price": {}},
                {"stock": None, "price": {}},
                {"stock": None, "price": {}},
                {"stock": None, "price": {}},
            ],
        }
    ]
    assert get_views("2021-12-02 00:00:00") == json.dumps(result, indent=4, ensure_ascii=False)
