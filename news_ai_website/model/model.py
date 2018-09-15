import pandas as pd
import numpy as np
import sklearn
from project import getPolarityVector
from keras.models import Model, Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.models import load_model
from urllib.parse import urlparse


# Function to predict
def predict(model, title, text, publisher):

    publishers = pd.read_csv('publishers.csv')
    title_vector = getPolarityVector(title, title=True).reshape((-1, 1))
    text_vector = getPolarityVector(text).reshape((-1, 1))
    index = 0
    
    for p in publishers.keys():
        if p == publisher:
            break
        index += 1

    print (index)

    publisher_vector = np.full((len(publishers.keys()), 1), 0)

    if index != (len(publishers.keys())): 
        vector = np.zeros([(index), 1])
        one = np.array([])
        one = np.full((1, 1), 1)
        extra = np.full(((len(publishers.keys()) - index - 1), 1), 0)
        publisher_vector = np.concatenate((vector, one,  extra))
        print ('exists')
    
    vector = np.concatenate((publisher_vector, text_vector, title_vector))
    return model.predict(vector.T)

def get_model():
    # Defining the model
    model = Sequential()
    model.add(Dense(32, input_dim=115, activation='sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='mean_squared_error', optimizer='adamax', metrics=['accuracy'])
    model = load_model('deep_net_config_1.hdf5')
    return model