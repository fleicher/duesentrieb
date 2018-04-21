import requests
from duesentrieb.constants import CONTROL_CMDS, TABLE_CMDS

with open("auth/key.txt") as f:
    key = f.read()
with open("auth/server.txt") as f:
    server = f.read()
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key,
}


class Intent:

    @staticmethod
    def getIntent(phrase):
        params = {
            # Query parameter
            'q': phrase,
            # Optional request parameters, set to default values
            'timezoneOffset': '0',
            'verbose': 'false',
            'spellCheck': 'false',
            'staging': 'false',
        }

        try:
            r = requests.get(server, headers=headers, params=params)
            # print(r.json())
            return r.json()["topScoringIntent"]["intent"]
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return None

    def __init__(self, phrase):
        self.phrase = phrase
        self.intent = Intent.getIntent(phrase)

    def isCommand(self, cmd):
        if cmd in CONTROL_CMDS:
            if self.intent == CONTROL_CMDS[cmd]:
                return True

        if cmd in TABLE_CMDS:
            if self.intent == TABLE_CMDS[cmd]:
                return True

        return False
