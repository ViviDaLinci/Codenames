import requests
import random

with open("wordlist-eng.txt", "r") as f:
    full_wordlist = f.readlines()
    full_wordlist = [line.rstrip() for line in full_wordlist]

current_wordlist = random.sample(full_wordlist, 25)
for i in range(len(current_wordlist)):
    current_wordlist[i] = current_wordlist[i].lower()
wordlist = current_wordlist

# Rote Wörter rausfiltern
red_words = random.sample(current_wordlist, 9)
update_list = set(red_words)
current_wordlist = [x for x in current_wordlist if x not in update_list]
# Blaue Wörter rausfiltern
blue_words = random.sample(current_wordlist, 8)
update_list = set(blue_words)
current_wordlist = [x for x in current_wordlist if x not in update_list]
# Weiße Wörter rausfiltern
white_words = random.sample(current_wordlist, 7)
update_list = set(white_words)
current_wordlist = [x for x in current_wordlist if x not in update_list]
# Schwarzes Wort rausfiltern
black_word = random.sample(current_wordlist, 1)
update_list = set(black_word)
current_wordlist = [x for x in current_wordlist if x not in update_list]

api_url = "https://api.conceptnet.io/query?node=/c/en/"
query = "&rel=/r/RelatedTo&offset=0&limit=1000"
print()
dict_red = {}
for i in red_words:
    response = requests.get(api_url + i + query)
    asJson = response.json()
    related = asJson["edges"]
    testarray_red = []
    for x in related:
        word = x["end"]["label"]
        if word != i and word not in testarray_red and " " not in word:
            testarray_red.append(word)

    for ab in testarray_red:
        isThere = dict_red.get(ab)
        if isThere == None:
            dict_red[ab] = 1
        else:
            oldValue = dict_red[ab]
            newValue = oldValue + 1
            dict_red[ab] = newValue
dict_red_sorted = sorted(dict_red.items(), key=lambda x: x[1], reverse=True)
dict_red_sorted_names = []
for i in dict_red_sorted:
    dict_red_sorted_names.append(i[0])

dict_blue = {}
testarray_blue = []
for i in blue_words:
    response = requests.get(api_url + i + query)
    asJson = response.json()
    related = asJson["edges"]
    for x in related:
        word = x["end"]["label"]
        if word != i and word not in testarray_blue and " " not in word:
            testarray_blue.append(word)

    for ab in testarray_blue:
        isThere = dict_blue.get(ab)
        if isThere == None:
            dict_blue[ab] = 1
        else:
            oldValue = dict_blue[ab]
            newValue = oldValue + 1
            dict_blue[ab] = newValue
dict_blue_sorted = sorted(dict_blue.items(), key=lambda x: x[1], reverse=True)
dict_blue_sorted_names = []
for i in dict_blue_sorted:
    dict_blue_sorted_names.append(i[0])

dict_white = {}
testarray_white = []
for i in white_words:
    response = requests.get(api_url + i + query)
    asJson = response.json()
    related = asJson["edges"]
    for x in related:
        word = x["end"]["label"]
        if word != i and word not in testarray_white and " " not in word:
            testarray_white.append(word)

    for ab in testarray_white:
        isThere = dict_white.get(ab)
        if isThere == None:
            dict_white[ab] = 1
        else:
            oldValue = dict_white[ab]
            newValue = oldValue + 1
            dict_white[ab] = newValue
dict_white_sorted = sorted(dict_white.items(), key=lambda x: x[1], reverse=True)
dict_white_sorted_names = []
for i in dict_white_sorted:
    dict_white_sorted_names.append(i[0])

dict_black = {}
testarray_black = []
for i in black_word:
    response = requests.get(api_url + i + query)
    asJson = response.json()
    related = asJson["edges"]
    for x in related:
        word = x["end"]["label"]
        if word != i and word not in testarray_black and " " not in word:
            testarray_black.append(word)

    for ab in testarray_black:
        isThere = dict_black.get(ab)
        if isThere == None:
            dict_black[ab] = 1
        else:
            oldValue = dict_black[ab]
            newValue = oldValue + 1
            dict_black[ab] = newValue
dict_black_sorted = sorted(dict_black.items(), key=lambda x: x[1], reverse=True)
dict_black_sorted_names = []
for i in dict_black_sorted:
    dict_black_sorted_names.append(i[0])

for x in dict_red_sorted:
    if x[0] not in red_words and x[0] not in dict_blue_sorted_names and x[0] not in dict_white_sorted_names and x[0] not in dict_black_sorted_names:
        print(x)
        break
