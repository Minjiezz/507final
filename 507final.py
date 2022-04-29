
#####################################
####### final project
####### Name: Minjie Zhao
#####################################


import requests
import json
import time
import numpy as np
import plotly.express as px
import pandas as pd


true_answers = ["yes", "y", "yup", "sure", "correct"]
false_answers = ["no", "n", "nope", "nah", "wrong"]


#####################################
####tree
#####################################

questionTree = \
    ("Do you want to know the minimum and maximum temperature for each day (enter '1') or see the temperature change for each day (enter '2')?",
        ("Show the minimum and maximum temperature for next week:", None, None),
        ("Show the day temperature changes for next week:", None, None))

def printTree(tree, prefix = '', bend = '', answer = ''):
    """Recursively print a 20 Questions tree in a human-friendly form.
       TREE is the tree (or subtree) to be printed.
       PREFIX holds characters to be prepended to each printed line.
       BEND is a character string used to print the "corner" of a tree branch.
       ANSWER is a string giving "Yes" or "No" for the current branch."""
    text, left, right = tree
    if left is None  and  right is None:
        print(f'{prefix}{bend}{answer}It is {text}')
    else:
        print(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree(left, prefix, '+-', "Yes: ")
        printTree(right, prefix, '`-', "No:  ")


def simplePlay(tree):

    node, left, right = tree
    answer = input(f"\n{node}")
    if int(answer) == 1:
        print(f'{left[0]}/n')
        return True
    if int(answer) == 2:
        print(f'{right[0]}/n')
        return False

#####################################
####current weather by city name
#####################################

# city_name = input(f"Which city do you want to search for weather?")
# API_key_current_weather = "d2e179d7f6dca72d1c5bcd4c1fb69d96"
# search_by_city_name_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key_current_weather}"
# weather_response = requests.get(search_by_city_name_url)
# current_weather = json.loads(weather_response.text)

# print(current_weather)

# city_weather = json.dumps(current_weather, indent=4)
# city_weather_file = open("city_weather.json", "w")
# city_weather_file.write(city_weather)
# city_weather_file.close()

#####################################
####weather forecast by city name
#####################################

# cnt = input(f"How many days weather forecast do you want to search? (up to 16 days)")
# API_key_weather_forecast = "d2e179d7f6dca72d1c5bcd4c1fb69d96"
# search_weather_forecast_url = f"https://api.openweathermap.org/data/2.5/forecast/daily?q={city_name}&cnt={cnt}&appid={API_key_weather_forecast}"
# forecast_response = requests.get(search_weather_forecast_url)
# weather_forecast = json.loads(forecast_response.text)

# print(weather_forecast)

# city_weather_forecast = json.dumps(weather_forecast, indent=4)
# city_weather_forecast_file = open("city_weather_forecast.json", "w")
# city_weather_forecast_file.write(city_weather_forecast)
# city_weather_forecast_file.close()

#####################################
####cache
#####################################

headers = {}
CACHE_FILE_NAME = ""
def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

#####################################
####weather class
#####################################

class Weather:

    def __init__(self, temp="", condition="", description="", feels_like="", temp_min='', temp_max='', pressure='', humidity='', windspeed= "", sunrise="", sunset="", json=None):

        if json:

            condition = json["weather"][0]['main']
            description = json["weather"][0]['description']
            temp = int(json["main"]["temp"] - 273.15)
            feels_like = int(json["main"]["feels_like"] - 273.15)
            temp_min = int(json["main"]["temp_min"] - 273.15)
            temp_max = int(json["main"]["temp_max"] - 273.15)
            pressure = int(json["main"]["pressure"])
            humidity = int(json["main"]["humidity"])
            windspeed = int(json["wind"]["speed"])
            sunrise = time.strftime("%I:%M:%S", time.gmtime(int(json["sys"]["sunrise"]) - 14400))
            sunset = time.strftime("%I:%M:%S", time.gmtime(int(json["sys"]["sunset"]) - 14400))

        self.condition = condition
        self.description = description
        self.temp = temp
        self.feels_like = feels_like
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.humidity = humidity
        self.windspeed = windspeed
        self.sunrise = sunrise
        self.sunset = sunset

    def info(self):
        return f'\nThe weather condition is: {self.condition}  \nThe description is: {self.description} \nThe temperature is: {self.temp}°C\n'

    def moreinfo(self):
        return f"\nThe mininum temperature is: {self.temp_min}°C \nThe maxinum temperature is: {self.temp_max}°C \nThe pressure is: {self.pressure}mb \nThe humidity is: {self.humidity}% \nThe windspeed is: {self.windspeed}km/h \nThe sunrise time is: {self.sunrise}am \nThe sunset time is: {self.sunset}pm\n"

#####################################
####weather forecast class
#####################################

class Forecast:

    def __init__(self, day_temp="", night_temp="", eve_temp="", morn_temp="", temp_min='', temp_max='', json=None):

        if json:

            day_temp = int(json["temp"]["day"] - 273.15)
            night_temp = int(json["temp"]["night"] - 273.15)
            eve_temp = int(json["temp"]["eve"] - 273.15)
            morn_temp = int(json["temp"]["morn"] - 273.15)
            temp_min = int(json["temp"]["min"] - 273.15)
            temp_max = int(json["temp"]["max"] - 273.15)

        self.day_temp = day_temp
        self.night_temp = night_temp
        self.eve_temp = eve_temp
        self.morn_temp = morn_temp
        self.temp_min = temp_min
        self.temp_max = temp_max

    def minandmax(self):
        return f'Minimum & maximum temperature of the day: {self.temp_min}°C & {self.temp_max}°C'

    def tempchange(self):
        return f"The temperature change from morning, noon, evening to night is: {self.morn_temp}°C, {self.day_temp}°C, {self.eve_temp}°C, {self.night_temp}°C"

def main():

    city_name = None

    while True:

        if city_name is None:
            city_name = input(f"Which city do you want to search for weather?")
            API_key_current_weather = "d2e179d7f6dca72d1c5bcd4c1fb69d96"
            search_by_city_name_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key_current_weather}"
            weather_response = requests.get(search_by_city_name_url)
            current_weather = json.loads(weather_response.text)

            city_weather = json.dumps(current_weather, indent=4)
            city_weather_file = open("city_weather.json", "w")
            city_weather_file.write(city_weather)
            city_weather_file.close()

        if city_name.lower() == "exit" or city_name.lower() in false_answers:
            break

        current_city_weather = Weather(json=current_weather)
        print(current_city_weather.info())

        more_info = None

        while True:

            if more_info is None:
                more_info = input(f"Do you want to know other information of the today's weather?")
                if more_info.lower() in true_answers:
                    print(current_city_weather.moreinfo())
                if more_info.lower() == "exit" or more_info.lower() in false_answers:
                    city_name = more_info
                    break

            next_week_weather = None

            while True:
                if next_week_weather is None:
                    next_week_weather = input(f"Do you want to search the weather forecast for next week of the city?")
                    if next_week_weather.lower() in true_answers:
                        API_key_weather_forecast = "d2e179d7f6dca72d1c5bcd4c1fb69d96"
                        search_weather_forecast_url = f"https://api.openweathermap.org/data/2.5/forecast/daily?q={city_name}&cnt=7&appid={API_key_weather_forecast}"
                        forecast_response = requests.get(search_weather_forecast_url)
                        weather_forecast_write = json.loads(forecast_response.text)
                        weather_forecast = json.loads(forecast_response.text)["list"]

                        city_weather_forecast = json.dumps(weather_forecast_write , indent=4)
                        city_weather_forecast_file = open("city_weather_forecast.json", "w")
                        city_weather_forecast_file.write(city_weather_forecast)
                        city_weather_forecast_file.close()

                    if next_week_weather.lower() == "exit" or next_week_weather.lower() in false_answers:
                        city_name = next_week_weather

                    list_of_weather_forecast = []

                    for forecast in weather_forecast:
                        weather_forecast_each_day = Forecast(json=forecast)
                        list_of_weather_forecast.append(weather_forecast_each_day)

                    choice = simplePlay(questionTree)

                    if choice:
                        for item in list_of_weather_forecast:
                            print(item.minandmax())
                    if choice is False:
                        for item in list_of_weather_forecast:
                            print(item.tempchange())

                see_graph = None

                while True:
                    if see_graph is None:
                        see_graph = input(f"\nWould you like to see a graph for temperature change next week in {city_name.title()}?")
                        if see_graph.lower() in true_answers:

                            list_of_temperature_next_week = []

                            API_key_weather_forecast = "d2e179d7f6dca72d1c5bcd4c1fb69d96"
                            search_weather_forecast_url = f"https://api.openweathermap.org/data/2.5/forecast/daily?q={city_name}&cnt=7&appid={API_key_weather_forecast}"
                            forecast_response = requests.get(search_weather_forecast_url)
                            weather_forecast = json.loads(forecast_response.text)["list"]

                            for forecast in weather_forecast:
                                weather_forecast_each_day = Forecast(json=forecast)
                                list_of_temperature_next_week.append((weather_forecast_each_day.temp_max + weather_forecast_each_day.temp_min)/2)

                            df = pd.DataFrame(dict(
                                Days = [1, 3, 2, 4, 5, 6, 7],
                                Temperature = list_of_temperature_next_week
                            ))
                            df = df.sort_values(by="Days")
                            fig = px.line(df, x="Days", y="Temperature", title=f"Temperature changes next week in {city_name.title()}")
                            fig.show()
                            print("Bye!")

                        if see_graph.lower() == "exit" or see_graph.lower() in false_answers:
                            city_name = see_graph
                            print("Bye!")

    print("Bye!")

if __name__ == '__main__':
    main()

