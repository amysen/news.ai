import nltk
import pandas as pd
import numpy as np
import re
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import LabelEncoder
import keras
from keras.utils import np_utils
# Vader Sentiment method from:
#   Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
# Sentiment Analysis of Social Media Text. Eighth International Conference on
# Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

# Applies normalization functions to data at a given column
def applyFunctions(data, column):
    data[column] = data[column].apply(lambda x : str(x).lower())
    data[column] = data[column].apply(lambda x: re.sub('[^a-z0-9\s.]', '', x))
    return data

# Tokenizes texts
def tokenizeTexts(data, column):
    for i in range(0, len(data[column])):
        data[column].iloc[i] = tokenize.sent_tokenize(data[column].iloc[i])
    return data

# Tokenizes a single text string
def tokenizeText(text):
    return tokenize.sent_tokenize(text)

# Tokenizes titles
def tokenizeTitles(data, column):
    for i in range(0, len(data[column])):
        data[column].iloc[i] = [data[column].iloc[i]]
    return data
# Tokenizes a single title string
def tokenizeTitle(title):
    return [title]

# Analysis and returns a polarity score
def analysePolarity(text, title=False):
    sentences = []

    if title:
        sentences = tokenizeTitle(text)
    else:
        sentences = tokenizeText(text)

    polarity = 0.
    sid = SentimentIntensityAnalyzer()
    for sentence in sentences:
            ss = sid.polarity_scores(sentence)
            polarity = polarity + ss['compound']
    
    if (len(sentences) != 0):
        polarity

    return polarity
    
def analyseData(data, name='new'):

    polarity_data = []
    sid = SentimentIntensityAnalyzer()
    for list in data[name].iloc[:len(data)-1]:
        polarity = 0.
        for sentence in list:
            ss = sid.polarity_scores(sentence)
            polarity = polarity + ss['compound']
        if (len(list) != 0):
            polarity = polarity / len(list)
            polarity_data.append(polarity)

    print ('Analyzed')
    return pd.Series(polarity_data)
        
# Returns a vector representing the qualitative polarity of a text/title
def getPolarityVector(text, title=False):
    x = analysePolarity(text, title)
    
    if (x < -0.7): 
        return np.array([1,0,0,0,0,0,0])
    elif (x >= -0.7) & (x < -0.4):
        return np.array([0,1,0,0,0,0,0])
    elif (x >= -0.4) & (x <  -0.1):
        return np.array([0,0,1,0,0,0,0])
    elif (x >= -0.1) & (x <=  0.1):
        return np.array([0,0,0,1,0,0,0])
    elif (x > 0.1) & (x <=  0.4):
        return np.array([0,0,0,0,1,0,0])
    elif (x > 0.4) & (x <= 0.7):
        return np.array([0,0,0,0,0,1,0])
    else:
        return np.array([0,0,0,0,0,0,1])

class VDA:

    def __init__(self):
        self.raw_data = pd.read_csv('fake.csv')
        self.pp_data = pd.DataFrame()
        self.pp_text = []
        self.sid = SentimentIntensityAnalyzer()
    
    def addUnbiasedData(self):
        print ("Appending...")
        self.ub_data = self.ub_data.rename({'headline': 'title', 'webURL':'site_url', 'snippet':'text'}, axis='columns')
        initial_data = self.ub_data
        self.ub_data = self.ub_data.where(initial_data['typeOfMaterial'] == 'News')
        self.ub_data.append(self.ub_data.where(initial_data['typeOfMaterial'] == 'OpEd'))
        self.ub_data = self.ub_data[['title', 'site_url', 'text', 'keywords']]
        print ("Concatenating...")
        self.pp_data = pd.concat([self.pp_data, self.ub_data], axis=0, ignore_index=True)
        print ("Applying Functions...")
        self.pp_data['text'] = applyFunctions(self.pp_data, 'text')
        self.pp_data['title'] = applyFunctions(self.pp_data, 'title')

        print ("Tokenizing texts...")
        # Tokenize title and text
        self.pp_data['text'] = tokenizeTexts(self.pp_data, 'text')

        print ("Tokenizing titles...")
        self.pp_data['text'] = tokenizeTitles(self.pp_data, 'title')

        print ("Analyzing...")
        # Sentiment Analysis
        self.pp_data = self.analyse(data=self.pp_data, name='text')
        self.pp_data = self.analyse(data=self.pp_data, name='title', new_column='title_polarity')
        print (len(self.pp_data))

        print ("Vectorizing...")
        # Vectorize and rename type
        self.pp_data['type'] = self.pp_data['type'].apply(lambda x : 1 if (x == 'bias') | (x == 'fake') | (x == 'bs') else 0)
        self.pp_data = self.pp_data.rename(columns={'type':'bias'})
        #self.pp_data = self.pp_data.drop('Unnamed: 0', axis=1)
        print ("Done")
        return self

    def clean(self):
        nltk.download('punkt')
        nltk.download('vader_lexicon')  

        self.pp_data = self.raw_data[['author', 'title', 'text', 'site_url', 'domain_rank', 'type']]

        bias_data = self.pp_data.where(self.pp_data['type'] == 'bias').dropna()
        bias_data = bias_data.append(self.pp_data.where(self.pp_data['type'] == 'fake').dropna())
        bias_data = bias_data.append(self.pp_data.where(self.pp_data['type'] == 'hate').dropna())
        bias_data = bias_data.append(self.pp_data.where(self.pp_data['type'] == 'bs').dropna())
        bias_data = bias_data.append(self.pp_data.where(self.pp_data['type'] == 'junksci').dropna())
        bias_data['type'] = bias_data['type'].apply(lambda x : 'bias' if x != 'bias' else x)
        self.pp_data = bias_data
        #bias_data = bias_data.drop('Unnamed: 0', axis=1)
        return self


    def analyse(self, data, name='new', new_column='text_polarity'):

        polarity_data = []

        for list in data[name].iloc[:len(data)-1]:
            polarity = 0.
            for sentence in list:
                ss = self.sid.polarity_scores(sentence)
                polarity = polarity + ss['compound']
            if (len(list) != 0):
                polarity = polarity / len(list)
                polarity_data.append(polarity)

        data[new_column] = pd.Series(polarity_data)
        print ('Analyzed')
        return data
        
    def saveProcessedData(self):
        self.pp_data[['author', 'title', 'site_url', 'text_polarity', 'title_polarity', 'bias']].to_csv('processed_data.csv', index=False)
        print ('Text Polarity Added to Dataframe.')
