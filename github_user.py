import requests


response = requests.get("https://api.github.com/users/abhinayjangde")
print(len(response.json()))