import nltk
import pandas as pd
import numpy as np
import re
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def clean():
    nltk.download('punkt')
    nltk.download('vader_lexicon')

    raw_data = pd.read_csv('fake.csv')
    pp_data = raw_data[['author', 'title', 'text', 'site_url', 'domain_rank', 'type']]
    pp_text = pp_data['text'].apply(lambda x : str(x).lower())
    pp_text = pp_text.apply(lambda x: re.sub('[^a-z0-9\s.]', '', x))

    for i in range(0, len(pp_text)):
        pp_text[i] = tokenize.sent_tokenize(pp_text[i])

    print pp_text.head()
