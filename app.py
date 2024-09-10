import requests

URL = "http://host3.dreamhack.games:12404/api/memo"

headers = {
    'API-KEY': 'vftsvmcs'
}

res = requests.get(URL, headers=headers)

print(res.text)