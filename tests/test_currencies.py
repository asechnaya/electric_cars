from datetime import date

import requests

BASE_LINK = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/"


def test_negative_currency():
    currency = "irregular"
    link = BASE_LINK + f"{date.today()}/currencies/usd/{currency}.json"
    response = requests.get(link)
    assert response.status_code == 403

