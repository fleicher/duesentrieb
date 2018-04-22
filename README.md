# RocketScience

## Overview
RocketScience is a prototype for an innovative platform that allows laymen to be guided doing tasks in a hands-free manner. 
It uses the Azure Luis service to hold conversations with a user and detect the users intents in natural spoken language.
It includes a user feedback loop to rate the instructions steps on the fly.

## Packages to install
To run the "Rocket Science" script you have to install
* PyAudio and SpeechRecognition (to detect spoken language in Python locally)
* simpleaudio  (to play sound file by Bing)
```bash
pip3 install -r requirements.txt
```

## Microsoft Azure Services
This Service is hooked up to Microsoft Azure. You need the following services: 
* Bing Speech (to do text to speech conversion)
* Azure Luis (to detect intends in the user's commands) A sample of utterances has to be provided at https://eu.luis.ai/ (url applies if you are operating a service for the EU)

You will need api keys for that. To get those go to  
* https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview for a free trial version
* https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0 for a professional paid version of the services by Azure

These keys shall then be stored in a json file in the folder auth/ which should look like this:
```json
{
  "bing-speech": "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "luis": "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "luis-app-id": "XXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

The Luis utterance database is stored in luis_model.json.

## Database

A database with all the instructions has to be stored in constants.DB_NAME. 
There is a small default sqlite table provided in duesentrieb.db You can also create your own mock table by executing:
```bash
python3 create_bike_test_db.py
``` 
The content of this small sample Database can be seen in the files content.csv and structure.csv


## Usage

To start the listening server, execute:
```bash
python3 main.py
```

The user can then via a speech interface send search requests to the instructions database for hands-free assistance on reqested tasks. 
Once a task is selected the user can talk RocketScience through the instruction steps.
After each step the user can rate the instructions given and ask for a different version (if one is provided)
