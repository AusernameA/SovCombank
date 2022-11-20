import json
import requests

with open("currency.json", 'r') as file:
    data = json.loads(file.read())
    currencies = json.loads(data)['currencies']

request_data = ''
for i in currencies:
    request_data += i + ', '

req = requests.get(f"https://api.apilayer.com/currency_data/live?base=RUB&symbols={request_data}",
             headers={'apikey' : 'SMNjaBEc5G3jtEUVQJx2bqsWe55oeRtN'})

data = req.text
print(data)

with open("price.json", 'a') as file:
    json.dump(data, file)

