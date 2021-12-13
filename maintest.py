import random
import os
from enum import Enum
import sys
import requests
api_url = 'http://api.conceptnet.io/'
concept = 'c/' # '/r'
lang = 'en/'

cat = requests.get(api_url + concept + lang + 'cat').json()
y = []
edges = cat["edges"]
for e in edges:
    if e["rel"]["label"] == "RelatedTo":
        y.append(e['end']['label'])

print(y[0])