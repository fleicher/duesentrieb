#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr


def getInput(use_speech=True, anounce=""):
    if use_speech:

        while True:
            # Record Audio
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print(anounce, "Say something:")
                # audio = r.record(source=source, duration=5)
                audio = r.listen(source)

            # Speech recognition using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                txt = r.recognize_google(audio, language="en-US")
                print("You said: " + txt)
                return txt
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    else:
        return input(anounce)
