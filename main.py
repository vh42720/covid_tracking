from covid_tracking.config.config import *

import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time

# Retrieve keys
API_KEY = API_KEY
PROJECT_TOKEN = PROJECT_TOKEN


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            'api_key': self.api_key,
        }
        self.data = self.get_data()

    def get_data(self):
        r = requests.get(f'https://parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                         params=self.params)
        data = json.loads(r.text)
        return data

    def get_total_cases(self):
        temp = [i['value'] for i in self.data['total'] if i['name'] == 'Coronavirus Cases:']
        return temp[0]

    def get_total_deaths(self):
        temp = [i['value'] for i in self.data['total'] if i['name'] == 'Deaths:']
        return temp[0]

    def get_total_recovered(self):
        temp = [i['value'] for i in self.data['total'] if i['name'] == 'Recovered:']
        return temp[0]

    def get_country_data(self, country):
        try:
            temp = [i for i in self.data['country'] if i['name'].lower() == country.lower()]
            return temp[0]
        except Exception as e:
            print('Exception:', e)

    def get_country_list(self):
        countries = [i['name'].lower() for i in self.data['country']]
        return countries

    def update_data(self):
        r = requests.post(f'https://parsehub.com/api/v2/projects/{self.project_token}/run',
                          params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print('Data updated!')
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print('Exception:', str(e))

    return said.lower()


def main():
    print("Started Program")
    data = Data(API_KEY, PROJECT_TOKEN)
    END_PHRASE = 'stop'
    country_list = data.get_country_list()

    TOTAL_PATTERNS = {
        re.compile(r"[\w\s]* total [\w\s]* case[s]?"): data.get_total_cases,
        re.compile(r"[\w\s]* total case[s]?"): data.get_total_cases,
        re.compile(r"total case[s]?[\w\s]*"): data.get_total_cases,
        re.compile(r"[\w\s]* total [\w\s]* death[s]?"): data.get_total_deaths,
        re.compile(r"[\w\s]* total death[s]?"): data.get_total_deaths,
        re.compile(r"total death[s]?[\w\s]*"): data.get_total_deaths,
    }

    COUNTRY_PATTERNS = {
        re.compile(r"[\w\s]* case[s]?[\w\s]*"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile(r"[\w\s]* death[s]?[\w\s]*"): lambda country: data.get_country_data(country)['total_deaths'],
    }

    UPDATE_COMMAND = 'update'

    while True:
        print("Listening...")
        text = get_audio()
        print(text)
        result = "I don't understand!"

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(' '))
                result = [func(word) for word in words if word in country_list][0]
                print(result)
                break

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        if text == UPDATE_COMMAND:
            result = 'Data is being updated. This may take a moment!'
            data.update_data()

        if text.find(END_PHRASE) != -1:
            print('Exit')   # stop loop
            break

        if result:
            speak(result)


main()
