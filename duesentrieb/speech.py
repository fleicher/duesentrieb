#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
import pyttsx3

import requests
from duesentrieb.constants import CONTROL_CMDS


def getInput(use_speech=True, anounce=""):
    if use_speech:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Speak now:", anounce)

        while True:
            # Record Audio
            with sr.Microphone() as source:
                if anounce != "":
                    say(anounce)
                # audio = r.record(source=source, duration=5)
                try:
                    audio = r.listen(source, timeout=1,phrase_time_limit=3)
                except sr.WaitTimeoutError as e:
                    print("-")
                    continue
            print(".")

            # Speech recognition using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                txt = r.recognize_google(audio, language="en-US")
                return txt
            except LookupError:
                print("Couldn't understand audio")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except Exception as e:
                print("general:", e)
    else:
        return input(anounce)


def say(text):
    engine = pyttsx3.init()
    print("saying:", text)
    engine.say(text)
    engine.runAndWait()


with open("auth/key.txt") as f:
    key = f.read()
with open("auth/server.txt") as f:
    server = f.read()
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key,
}


class Intent:

    def __init__(self, use_speech=True, anounce=""):
        self.phrase = getInput(use_speech=use_speech, anounce=anounce)
        params = {
            # Query parameter
            'q': self.phrase,
            # Optional request parameters, set to default values
            'timezoneOffset': '0',
            'verbose': 'false',
            'spellCheck': 'false',
            'staging': 'false',
        }

        try:
            r = requests.get(server, headers=headers, params=params)
            # print(r.json())
            self.intent = r.json()["topScoringIntent"]["intent"]
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            self.intent =  None

        print("You said: " + self.phrase, "->", self.intent)

    def isCommand(self, cmd):
        if cmd in CONTROL_CMDS:
            if self.intent == CONTROL_CMDS[cmd]:
                return True

        return False

    def __repr__(self):
        return "<Intent " + self.intent + ">"