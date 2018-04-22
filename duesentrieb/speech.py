"""
Handle the speech or textual input and redirect them to the Azure server.
"""
import http.client
import simpleaudio
import json
import requests
import speech_recognition as sr
from xml.etree import ElementTree

from duesentrieb.constants import be_quiet, INTENT_CERTAINTY_THESHOLD


def get_command(announce=""):
    # type: (str) -> str
    """
    ask the user what they want to do next. Before listening the announce text is played
    PyAudio is used to get the microphone input of the user
    Google Speech Recognition is used to translate it into text, this text is then returned.
    """
    if not be_quiet:
        # use speech input
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Speak now:", announce)

        while True:
            # Record Audio
            with sr.Microphone() as source:
                if announce != "":
                    say(announce)
                try:
                    audio = r.listen(source, timeout=10, phrase_time_limit=5)
                except sr.WaitTimeoutError:
                    # reset the listener as otherwise the files can get to large for the Google Speech2Text service
                    continue
            # print("Detected voice")

            try:
                # Speech recognition using Google Speech Recognition
                txt = r.recognize_google(audio, language="en-US")
                return txt
            except sr.UnknownValueError:
                # print("This was just mumbeling, Google Speech Recognition could not understand audio")
                pass
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    else:
        return input(announce)


def say_azure(text):
    # type: (str) -> None
    """
    read aloud the given text via the Azure Bing Speech Service, original interface:
    https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/Samples-Http/Python/TTSSample.py
    """
    with open("auth/keys.json") as f:
        keys = json.load(f)
        api_key = keys["bing-speech"]

    params = ""
    headers = {"Ocp-Apim-Subscription-Key": api_key}

    # AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
    access_token_host = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    # Connect to server to get the Access Token
    # print("Connect to server to get the Access Token")
    conn = http.client.HTTPSConnection(access_token_host)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()

    data = response.read()
    conn.close()

    accesstoken = data.decode("UTF-8")

    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
    voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
    voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)')
    voice.text = text

    headers = {"Content-type": "application/ssml+xml",
               "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
               "Authorization": "Bearer " + accesstoken,
               "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
               "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
               "User-Agent": "TTSForPython"}

    # Connect to server to synthesize the wave
    conn = http.client.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
    response = conn.getresponse()

    # temporarily write sound as file and then play it TODO: do this directly
    data = response.read()
    conn.close()

    with open("tmp.wav", "wb") as f:
        f.write(data)
    with open("tmp.wav", "rb") as f:
        waveobject = simpleaudio.WaveObject.from_wave_file(f)
    waveobject.play()


def say_pyttsx(text):
    # type (str) -> None
    """ alternative method with local text2speech (worse quality)"""
    import pyttsx3

    engine = pyttsx3.init()
    print("saying:", text)
    engine.say(text)
    engine.runAndWait()


def say(text, use_azure=True):
    # type: (str, bool) -> None
    """ entry method for Text2Speech """
    print("saying:", text)
    if use_azure:
        say_azure(text)
    else:
        say_pyttsx(text)


class Intent:
    """ query the Azure server for a intent for the extracted command by the user."""
    def __init__(self, announce=""):
        self.phrase = get_command(announce=announce)
        params = {
            # Query parameter
            'q': self.phrase,
            # Optional request parameters, set to default values
            'timezoneOffset': '0',
            'verbose': 'false',
            'spellCheck': 'false',
            'staging': 'false',
        }
        self.intent = None
        self.score = None
        self.entities = []

        with open("auth/keys.json") as f:
            key = json.load(f)["luis"]

        server = "https://westeurope.api.cognitive.microsoft.com/luis/v2.0/apps/c5027c65-c894-4eac-abe2-186faf2f7262"
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': key,
        }
        try:
            r = requests.get(server, headers=headers, params=params)
            json_object = r.json()
            print("Received:", json_object)
            self.score = json_object["topScoringIntent"]["score"]
            if self.score < INTENT_CERTAINTY_THESHOLD:
                raise Exception
            self.intent = json_object["topScoringIntent"]["intent"]
            self.entities = json_object["entities"]

        except Exception:
            pass  # no intent found or the score is above threshold

        print("User said: " + self.phrase, "->", self.intent, "({score})".format(score=self.score))

    def is_command(self, cmd):
        # type: (str) -> bool
        """ Returns True if """
        return True if cmd == self.intent else False

    def __repr__(self):
        return "<Intent " + self.intent + ">"
