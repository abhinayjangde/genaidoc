import requests


response = requests.get("https://api.github.com/users/abhinayjangde")
print(dict(response.json()))