import os

import requests

params = {"apikey": os.environ["DJANGO_OMDB_KEY"], "t": "star wars"} 
resp = requests.get("https://www.omdbapi.com/", params=params)
# actual URL will be https://www.omdbapi.com/?apikey=<key>&t=star+wars

print(resp.json())
