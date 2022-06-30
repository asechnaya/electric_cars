import logging

import pytest
import requests

from main_urls import MAIN_URL
from utils import set_default_parking_voltage


@pytest.fixture(scope="function")
def api_connection():
    try:
        response = requests.get(MAIN_URL)
        if response.status_code != 200:
            logging.error("Ошибка, Код ответа: %s", response.status_code)
            raise 'Error'
        else:
            set_default_parking_voltage()
            yield
    except ConnectionError:
        logging.error("Ошибка ConnectionError")