
import time

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