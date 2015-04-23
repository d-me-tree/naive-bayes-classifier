import codecs
import re
from math import log
from pprint import pprint

# helper functions
def remove_punctuation(s):
    return re.sub(r'\. |: |\?|!|;|,', ' ', s)

def tokenize(text):
    text = remove_punctuation(text)
    text = text.lower()
    return re.split('\s+', text)

def count_words(words):
    wc = {}
    for word in words:
        if len(word) > 3:
            wc[word] = wc.get(word, 1.0) + 1.0
    return wc

# tweet = '[blog] Using Nullmailer and Mandrill for your Ubuntu Linux server outboud mail:  http://bit.ly/ZjHOk7  #plone'
# print count_words(tokenize(tweet))


# Read in csv files and create bag of words for each file
with codecs.open('../app.csv', 'r', encoding='latin-1') as f:
    tweets = f.read()
app = count_words(tokenize(tweets))

with codecs.open('../other.csv', 'r', encoding='latin-1') as f:
    tweets = f.read()
other = count_words(tokenize(tweets))

# Get the total word counts
app_total = sum(app.values())
other_total = sum(other.values())

# Calculate probabilities
log_prob_app = {}
log_prob_other = {}

for k,v in app.iteritems():
    log_prob_app[k] = log(v / float(app_total))

for k,v in other.iteritems():
    log_prob_other[k] = log(v / float(other_total))

# Test the model
results = []
with codecs.open('../test_set.csv', 'r', encoding='latin-1') as f:
    f.readline() # skip the header
    for row in f:
        no, label, tweet = row.strip().split(',', 2)
        tweet = tokenize(tweet)

        sum_app = 0
        sum_other = 0
        for word in tweet:
            if len(word) > 3:
                sum_app += log_prob_app.get(word, log(1.0 / app_total))
                sum_other += log_prob_other.get(word, log(1.0 / other_total))

        results.append((no, label, 'APP' if sum_app > sum_other else 'OTHER'))

pprint(results)
