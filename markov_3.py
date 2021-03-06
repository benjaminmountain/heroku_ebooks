import numpy as np
import twitter
import random
import re
import string
from local_settings import (MY_CONSUMER_KEY, MY_CONSUMER_SECRET, MY_ACCESS_TOKEN_KEY, MY_ACCESS_TOKEN_SECRET, DEBUG, ODDS)

# Adapted from https://towardsdatascience.com/simulating-text-with-markov-chains-in-python-1a27e6d13fc6
# And of course from heroku_ebooks page this project was forked from

def hasNumber(inputString):
    return bool(re.search(r'\d', inputString))

def connect(type='twitter'): # connect to twitter API using keys from developer account
    if type == 'twitter':
        return twitter.Api(consumer_key=MY_CONSUMER_KEY,
                       consumer_secret=MY_CONSUMER_SECRET,
                       access_token_key=MY_ACCESS_TOKEN_KEY,
                       access_token_secret=MY_ACCESS_TOKEN_SECRET,
                       tweet_mode='extended')
    return None


cars2 = open('cars2.txt', encoding='utf8').read()

corpus = cars2.split()

def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])

def generate_script(corpus):
    pairs = make_pairs(corpus)
    word_dict = {}

    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    first_word = np.random.choice(corpus)

    # Select new first word until it is capitalized and doesn't contain numbers
    while first_word.islower() or hasNumber(first_word):
        first_word = np.random.choice(corpus)
    chain = [first_word]

    n_words = random.randint(2, 6)
    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))

    return ' '.join(chain)

tweet = generate_script(corpus)
roll = 0
if ODDS and not DEBUG:
    roll = random.randint(0, ODDS - 1)

# Drop last word
tweet = re.sub(r'\s\w+.$', '', tweet)

# Remove all characters after punctuation (issue if word has apostrophe)
#
# Attributions
# https://www.geeksforgeeks.org/string-punctuation-in-python/
# https://stackoverflow.com/questions/904746/how-to-remove-all-characters-after-a-specific-character-in-python
# for i in tweet:
#     if i in string.punctuation:
#         head, sep, tail = tweet.partition(i)
#         tweet = head + sep
#         print("{} removed from tweet".format(tail))
#         break

for i in tweet:
    if i == ",":
        head, sep, tail = tweet.partition(i)
        tweet = head
        print("{} removed from tweet".format(tail))
        break
    if i == "'" or i == "(" or i == ")" or i == "-":
        break
    elif i in string.punctuation:
        head, sep, tail = tweet.partition(i)
        tweet = head + sep
        print("{} removed from tweet".format(tail))
        break



if not DEBUG and len(tweet) < 210 and not roll:
    api = connect()
    status = api.PostUpdate(tweet)

print(tweet)
