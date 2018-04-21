#! /usr/bin/env python3

# -*- coding: utf-8 -*-

import http.client, urllib.parse, json
from xml.etree import ElementTree
import simpleaudio


# Note: The way to get api key:
# Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
# Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0


def say_azure(text):
    with open("auth/keys.json") as f:
        keys = json.load(f)
        apiKey = keys["bing-speech"]


    params = ""
    headers = {"Ocp-Apim-Subscription-Key": apiKey}

    # AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    # Connect to server to get the Access Token
    # print("Connect to server to get the Access Token")
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()

    # print(response.status, response.reason)

    data = response.read()
    conn.close()

    accesstoken = data.decode("UTF-8")
    # print("Access Token: " + accesstoken)

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
    # print("\nConnect to server to synthesize the wave")
    conn = http.client.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
    response = conn.getresponse()
    # print(response.status, response.reason)

    data = response.read()
    with open("tmp.wav", "wb") as f:
        f.write(data)
    conn.close()
    # print("The synthesized wave length: %d" % (len(data)))

    with open("tmp.wav", "rb") as f:
        waveobject = simpleaudio.WaveObject.from_wave_file(f)
    waveobject.play()


# def get_text(blob_name):
#     from azure.storage.blob import BlockBlobService
#     # load speech file to process
#     blob_service = BlockBlobService(azure_storage_account_name, azure_storage_account_key)
#     blob = blob_service.get_blob_to_bytes(container_name, blob_name)
#
#     wav_bytes = Audio(data=blob)
#     display(wav_bytes)


if __name__ == "__main__":
    say_azure("This is my Test for Azure.")