import requests

api_key = "e5bfda86c59d40298ecb5297067630e9"

uri = "https://newsapi.org/v2/top-headlines?country=in&apiKey=e5bfda86c59d40298ecb5297067630e9"

r = requests.get(uri)

print(r.json())