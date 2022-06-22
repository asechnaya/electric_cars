import statistics
import time
from datetime import date, timedelta

import requests

BASE_LINK = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/"


def calculate_dependence(currency):
    x, y = [], []
    i = 30
    try:
        while i > 0:
            target_date = date.today() - timedelta(days=i)
            link = BASE_LINK + f"{target_date}/currencies/usd/{currency}.json"
            response = requests.get(link)
            if response.status_code != 200:
                print("Ошибка, Код ответа: %s", response.status_code)
                time.sleep(1)
                continue
            x.append(target_date.strftime("%d.%m"))
            y.append(response.json()[currency])
            i -= 1
        return x, y
    except ConnectionError:
        print("Ошибка ConnectionError")


def calculate_values(money):
    mean = round(statistics.mean(money), 2)
    maximum = round(max(money), 2)
    minimum = round(min(money), 2)
    return mean, maximum, minimum


def create_text(currency, mean, maximum, minimum):
    the_text = f'Comparison of currencies $/{currency}: ' \
               f'min  = {minimum}, ' \
               f'max = {maximum}, ' \
               f'mean = {mean} '
    return the_text
