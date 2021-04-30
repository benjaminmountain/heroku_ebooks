import numpy as np
import twitter
import random
from local_settings import (MY_CONSUMER_KEY, MY_CONSUMER_SECRET, MY_ACCESS_TOKEN_KEY, MY_ACCESS_TOKEN_SECRET, DEBUG)

# Adapted from https://towardsdatascience.com/simulating-text-with-markov-chains-in-python-1a27e6d13fc6

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

def generate_script(carpus):

    pairs = make_pairs(corpus)

    word_dict = {}

    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    first_word = np.random.choice(corpus)

    # Select new first work until it is capitalized
    while first_word.islower():
        first_word = np.random.choice(corpus)

    chain = [first_word]

    n_words = random.randint(5, 31)

    for i in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))

    return ' '.join(chain)


tweet = generate_script(corpus)

if not DEBUG and len(tweet) < 210:
    api = connect()
    status = api.PostUpdate(tweet)

print(tweet)
