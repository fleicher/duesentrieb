import requests
with open("auth/key.txt") as f:
    key = f.read()
with open("auth/server.txt") as f:
    server = f.read()
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key,
}

params ={
    # Query parameter
    'q': 'fix my tire',
    # Optional request parameters, set to default values
    'timezoneOffset': '0',
    'verbose': 'false',
    'spellCheck': 'false',
    'staging': 'false',
}

try:
    r = requests.get(server, headers=headers, params=params)
    print(r.json())

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
