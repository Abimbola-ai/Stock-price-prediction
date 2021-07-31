import requests
import json

url = 'http://127.0.0.1:5000/results'
resp = requests.post(url, data=json.dumps({"inputs":[["FB",2]]}))

print(json.loads(resp.text))