from datetime import date

import requests

from currencies import calculate_dependence

BASE_LINK = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/"


def test_negative_currency():
    currency = "irregular"
    link = BASE_LINK + f"{date.today()}/currencies/usd/{currency}.json"
    response = requests.get(link)
    assert response.status_code == 403


def test_negative_date():
    assert calculate_dependence('rub', n=-2) == 403


