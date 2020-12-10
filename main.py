"""
This is the main python module
"""
import time
import datetime
import sched
import logging
import json
import pyttsx3

from flask import Flask, render_template, request, redirect
from time_conversion import hhmm_to_seconds, current_time_hhmm
from notification import *


# setting up pyttsx3
engine = pyttsx3.init()

# setting up a log file
logging.getLogger('werkzeug').disabled = True
logging.basicConfig(filename="sys.log", level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# imports config file with the APis
with open('config.json', 'r') as f:
    json_file = json.load(f)
keys = json_file["API-keys"]  # imports api-keys from config file
location = json_file["location"]  # imports location from the config file
cases_and_deaths = json_file["cases_and_deaths"]  # obtains covid data from config file
unfilter = (news_API(keys, location))  # obtains a dictionary of articles
weather = weather_API(keys, location)
weather_info = weather["weather"]
temperature = weather["main"]
articles = unfilter["articles"]
covid_data = covid_API(cases_and_deaths)
covid_information = covid_data["data"]
#obtains a dictionary of notifications
filtered_notifications = notification_list(articles, weather_info, temperature, covid_information)

deleted_notifications = []
#  Setting up alarm clock variables
s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)

deleted_alarms = []
alarm = []
alarm_key = ['title', 'content', 'weather', 'news']
events = []


@app.route('/')
def go_to_index():
    """
    Redirects user to /index
    """
    logging.info("Application has been launched")
    return redirect('/index')


@app.route('/index')
def index():
    """
    Asks for user inputs and adds them to data structures
    """
    s.run(blocking=False)
    # asks for user input
    user_input_alarm = request.args.get('alarm')
    user_input_label = request.args.get('two')
    # changes the alarm depending on if these are implemented
    user_input_weather = request.args.get('weather')
    user_input_news = request.args.get('news')
    # adds user set alarm to list of dictionaries
    if user_input_alarm and user_input_label is not None:
        alarm_date = user_input_alarm[:10] + ' ' + user_input_alarm[11:]
        # converts time and date to datetime
        alarm_date_obj = datetime.datetime.strptime(alarm_date, '%Y-%m-%d %H:%M')
        alarm_hhmm = user_input_alarm[-5:-3] + ':' + user_input_alarm[-2:]
        delay = hhmm_to_seconds(alarm_hhmm) - hhmm_to_seconds(current_time_hhmm())
        alarm_list = list((user_input_label, user_input_alarm, user_input_weather, user_input_news))
        alarm_dict = dict(zip(alarm_key, alarm_list))
        alarm.append(alarm_dict)
        scheduler(alarm_dict, delay, alarm_date_obj)

    alarm_button = request.args.get('alarm_item')
    # this conditional will delete an alarm if the user has requested
    if alarm_button is not None:
        deleted_alarm(alarm_button)

    deleted = request.args.get('notif')
    # this conditional will delete a notification if user has requested
    if deleted is not None:
        deleted_notification(deleted)

    return render_template('index.html', title="Smart Alarm", alarms=alarm, image="alarm.png",
                           notifications=filtered_notifications)


def deleted_notification(notification: str) -> dict:
    """
    Will delete a notification if user has requested that to happen
    """
    for filtered_notification in filtered_notifications:
        if filtered_notification['title'] == notification:
            deleted_notifications.append(filtered_notification)
            filtered_notifications.remove(filtered_notification)
    return filtered_notifications


def deleted_alarm(user_alarm: str) -> list:
    """
    Deletes an alarm from dict and the scheduled event
    """

    for event in events:
        sched_alarm = event.get('alarm')
        sched_event = event.get('event')
        try:
            for x in range(len(sched_alarm)):
                if sched_alarm[x]['title'] == user_alarm:
                    s.cancel(sched_event)
                    logging.info("Alarm %s successfully removed from schedule", user_alarm)
        except ValueError:
            logging.error("Alarm event cannot be found")

    for labels in alarm:
        try:
            if labels['title'] == user_alarm:
                deleted_alarms.append(labels)
                alarm.remove(labels)
                logging.info("Alarm %s removed from visual alarm list", user_alarm)
        except ValueError:
            logging.error("Alarm cannot be found")
    return alarm


def scheduler(alarms: dict, delay: int, inputted_date) -> None:
    """"
    This function schedules alarms - prioritised by the , refreshes notifications every hour
    """
    current_date = datetime.date.today()
    date = inputted_date
    if date.date() == current_date:
        event_enter = {"alarm": alarm, "event": s.enter(int(delay), 1, announce, [current_alarm(alarms)])}
        print(event_enter.get('alarm'))
        events.append(event_enter)


def current_alarm(alarm_dict) -> str:
    """
Obtains data necessary for the alarm announcement
    """
    # calls covid stats from notification module
    covid_stats = covid_maths(covid_data["data"])

    if alarm_dict['weather'] or alarm_dict['news'] is not None:
        if alarm_dict['news'] is None:
            weather_data = weather_API(keys, location)
            current_weather = announce_weather(weather_data)
            return covid_stats + current_weather
        elif alarm_dict['weather'] is None:
            news_data = (news_API(keys, location))
            current_headlines = announce_news(news_data)
            return covid_stats + current_headlines
        else:
            weather_data = weather_API(keys, location)
            current_weather = announce_weather(weather_data)
            news_data = (news_API(keys, location))
            current_headlines = announce_news(news_data)
            return covid_stats + current_weather + current_headlines
    else:
        return covid_stats

def announce(announcement):
    """
This module will announce the text to speech and remove alarm once announced
    """
    try:
        engine.endLoop()
    except RuntimeError as runtime:
        logging.error(runtime)
    engine.say(announcement)
    engine.runAndWait()
    #deleted_alarms()


if __name__ == '__main__':
    app.run()




