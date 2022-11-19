import json
import requests


req = requests.get("https://api.apilayer.com/currency_data/list",
             headers={'apikey' : 'SMNjaBEc5G3jtEUVQJx2bqsWe55oeRtN'})

data = req.text
print(data)

with open("currency.json", 'a') as file:
    json.dump(data, file)

