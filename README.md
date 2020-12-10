#README

##Introduction
In the era of this Covid 19 Pandemic, keeping track of what is happening in the news, weather and 
with the numbers of the pandemic has been difficult.
This smart alarm allows you, the user, to set alarms using a simple HTML interface. 
These alarms are will announce the number of cases, deaths and growth rate of covid-19. 
One great feature is that when setting the alarm the are toggleable to announce the news and/or the weather. 
These briefings are announced via text to speech
On the right hand side there is a list of news, weather and covid statistics
so the user can passively read what is happening. 
On News Briefings there are hyperlinks so the user is able to read the full article. 

##Prerequisites
* Python 3.8 or higher 
* If it has not been installed you can install python [Here](https://www.python.org/) and make sure to install Python 3, not 2

##Installation
* API Keys - both of these require registration before using 
    * OpenWeatherAPI from [Here](https://openweathermap.org/api) - note it may take 10 mins to 2 hours for it to work
    * NewsAPI is from [Here](https://newsapi.org/)
    * Covid data is obtained through an installation of a python module

* Python Modules Required:
All installations can be complete on the terminal for example `pip install pyttsx3`
    * from uk_covid19 module import Cov19API
    * sched
    * flask
    * pyttsx3 
        *  this may need an installation of `pip install wheel` - from personal troubleshooting
    * pytest 
        
##Getting Started
Before anything can be run, the API keys, as well as location data needs to be updated to the config file.
The config file is set such that the weather and news strings contain your unique API key
```json
{
    "API-keys":{
        "weather": "<insert API key here>",
        "news" : "<insert API key here>"
    }
}
```
To change location for the weather API, the config file will also need input for the city. The list of cities can be found [Here.](https://openweathermap.org/current#name)
Enter the city location here in the config file.
```json
{
  "location": {
    "news_location": "gb",
    "city_location": "<Change location here>"
  }
}
```
Open up a terminal of your choice and locate to directory where package was downloaded. Simply run from terminal `python main.py` or if multiple
versions of python are installed `python3 main.py`. It will show a local network 127.0.0.1:5000 (make sure your port is 5000).\ 

To set an alarm simply enter it into the calendar along with a label. This will then appear on the left hand side. Clicking the crosses on 
either notifications or alarms will delete an alarm. It is as simple as that. 

##Testing

To test the code simply use `python -m pytest` at the terminal before use. Make sure that terminal is in the tests directory folder.
This will return whether a test has failed so that it can troubleshooted before program is launched\
Note: pytest must be installed as mentioned above. 

##Author's Note:
 
There are some known bugs in this implementation of this software release
* You cannot set two alarms of the same name - This is a known bug and it will be caught through a try/except block 
* Error will occur if user tries to set an alarm before the present
* You cannot add an alarm while tts is happening simultaneously
* Known bug on mac for there to be an error with pyttsx3 - nothing much can be done but is included in the errors. 


##Details
Author: Priya Shah\
Template: Matt Collinson\
License: MIT License
