"""
This module will obtain data from the APIs and filter the relevant news. It will also prepare alarm briefings
"""
import logging
import time
import requests

from uk_covid19 import Cov19API
from flask import Markup

england_only = [
    'areaType=nation',
    'areaName=England'
]

def covid_API(cases_and_deaths: dict) -> dict:
    """
    Imports Covid Data
    :param cases_and_deaths: This obtains dictionary from config file
    :return: A dictionary of covid information
    """
    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    data = api.get_json()
    return data

def covid_maths(data: list) -> str:
    """
    Will return whether the growth rate of covid-19 is positive for alarm announcements
    :param data: This a list of covid data for each day
    :return: A string detailing covid-19 information
    """
    first_date = data[0]['newCasesByPublishDate']
    second_date = data[1]['newCasesByPublishDate']

    number_of_cases = data[0]['newCasesByPublishDate']
    number_of_deaths = data[1]['newDeathsByDeathDate']

    try:
        growth_rate = ((first_date - second_date)/second_date) * 100
        if growth_rate > 0:
            return "the current of cases is " + str(number_of_cases) + ". The number of deaths as of yesterday is " + str(number_of_deaths) + " The growth rate is positive meaning the epidemic is growing."
        else:
            return "the current of cases is " + str(number_of_cases) + ". The number of deaths as of yesterday is " + str(number_of_deaths) + " The growth rate is negative, meaning the epidemic is shrinking."
    except ZeroDivisionError as division:  # try to divide by 0
        logging.error(division)
        return "API is not working currently"

def news_API(keys: dict, location: dict) -> dict:
    """
    Importing news API Information
    :param keys: Contains a dictionary of keys from the config file
    :param location: Contains a dictionary of locations from the config file
    :return: Returns a dictionary of top news headlines
    """
    news_api_key = keys["news"]
    base_news_url = "https://newsapi.org/v2/top-headlines?"
    news_location = location["news_location"]
    complete_news_url = base_news_url + "country=" + news_location + "&apiKey=" + news_api_key

    # log if error 401 occurs...
    try:
        news_data = (requests.get(complete_news_url).json())
        logging.info("success")
        return news_data
    except:
        logging.critical("Status has resulted in error, API has failed to be imported")
        return 1

def weather_API(keys: dict, location: dict) -> dict:
    """
    Import weather API information
    :param keys: Dictionary of keys from config file
    :param location: Dictionary of locations from config file
    :return: A dictionary of weather information
    """
    # importing weather information
    weather_api_key = keys["weather"]
    base_weather_url = "http://api.openweathermap.org/data/2.5/weather?"
    weather_city = location["city_location"]
    units = "metric"
    complete_weather_url = base_weather_url + "appid=" + weather_api_key + "&q=" + weather_city +"&units=" + units
    #  try except block to ensure that data is returned
    try:
        weather_data = (requests.get(complete_weather_url).json())
        logging.info("Weather API successfully returned data")
        return weather_data
    except:
        logging.error("Weather API did not successfully return data")
        return 1

def notification_list(articles: list, weather_info: list, temperature: list, covid: list) -> list:
    """
    This function will filter the news and return a list of dictionaries
    :param articles: A list of top headlines
    :param weather_info: A list of weather information
    :param temperature: A list containing temperature
    :param covid: A list containing covid information
    :return: Returns a list of dictionaries for notifications
    """
    key = ['title', 'content', 'date']
    notifications = []
    # this loop will add the articles to the notification data structure
    for article in articles:
        title = (article["title"])
        url = (article["url"])
        url = Markup("<a href=") + url + Markup("> Click Here </a>")
        time_created = (article["publishedAt"])
        article_list = list((title, url, time_created))
        articles_dict = dict(zip(key, article_list))
        notifications.append(articles_dict)

    # this adds weather to the list of notifications
    weather_title = "Hourly Weather Update"
    weather_temperature = temperature["temp"]
    weather_type = weather_info[0]["main"]
    weather_content = "The weather is currently: " + weather_type + " and the Current Temperature is: " + str(weather_temperature) + " degrees celsius"
    weather_time = time.asctime(time.gmtime())
    weather_list = list((weather_title, weather_content, weather_time))
    weather_dict = dict(zip(key, weather_list))
    notifications.insert(0, weather_dict)

    covid_date = covid[0]["date"]
    covid_cases = covid[0]["newCasesByPublishDate"]
    covid_deaths = covid[0]["newDeathsByDeathDate"]

    covid_title = "Covid Stats as of " + covid_date
    covid_content = "Total number of cases: " + str(covid_cases) + ". Total number of deaths: " + str(covid_deaths)

    covid_list = list((covid_title, covid_content, covid_date))
    covid_dict = dict(zip(key, covid_list))
    notifications.insert(0, covid_dict)

    return notifications

def announce_news(news: dict) -> str:
    """
    Function will get the top 5 headlines for tts
    :param news: The news dictionary
    :return: Top 5 headlines
    """

    news_announcement = []
    articles = news['articles']
    for _ in range(5):
        news_announcement.append(articles[_]['title'])
    top_headlines = '.'.join(news_announcement)
    return top_headlines

def announce_weather(weather: dict) -> str:
    """
    The function will get weather for text to speech
    :param: weather: Dictionary containing information for weather API
    :return: Current Weather and Temperature
    """
    # Obtains all weather data from API
    weather_list = weather['weather']
    current_weather = weather_list[0]['main']
    current_description = weather_list[0]['description']
    temperature_list = weather['main']
    temperature_feel = temperature_list['feels_like']
    current_temperature = temperature_list['temp']

    weather_announcement = "The current weather is " + current_weather + " . It is described as " + current_description + ". The current temperature is" + str(current_temperature) + "degrees celsius. However, it feels like" + str(temperature_feel)
    return weather_announcement






