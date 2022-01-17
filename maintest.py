import random
import requests

api_url = 'http://api.conceptnet.io/'
concept = 'c/' # '/r'
lang = 'en/'

red_words = ["fire"]
word_request = requests.get(api_url + concept + lang + random.choice(red_words)).json()

y = []
edges = word_request["edges"]
for e in edges:
    if e["rel"]["label"] == "RelatedTo":
        y.append(e['end']['label'])
clue = y[0]
print(clue)
