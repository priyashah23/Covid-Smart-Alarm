"""
This module tests the notification module to make sure API's are working
"""

from notification import news_API
from notification import weather_API

import json

def test_news_API() -> None:
    with open('config.json', 'r') as f:
        json_file = json.load(f)
    keys = json_file["API-keys"]  # imports api-keys from config file
    location = json_file["location"]  # imports location from the config file
    data = news_API(keys, location)
    assert data['status'] == 'ok'

def test_weather_API() -> None:
    with open('config.json', 'r') as f:
        json_file = json.load(f)
    keys = json_file["API-keys"]  # imports api-keys from config file
    location = json_file["location"]  # imports location from the config file
    data = weather_API(keys, location)
    assert data['cod'] == 200

