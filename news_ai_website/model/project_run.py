import pandas as pd
import numpy as np
import sklearn
from project import VDA
from project import getPolarityVector
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from keras.callbacks import EarlyStopping
from keras.models import Model, Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.models import load_model
from keras.models import save_model
from urlparse import urlparse
import h5py
# Setting up comet_ml
# experiment = Experiment(api_key="C0PAAWMRSoTYzQ3wkCYc0jywY",
#                         project_name="KainosHackathon", workspace="goinhasf")

# Instances
vda = VDA()
pp_data = pd.DataFrame()

def pre_process_data():

    vda.clean()
    vda.addUnbiasedData()
    vda.saveProcessedData()

# Loads and prepares the processed_data for fitting
def loadAndPrepare():

    pp_data = pd.read_csv('processed_data.csv')
    pp_data = pd.concat([pp_data, pd.read_csv('unbiasedData.csv')]).reset_index()
    pp_data = pp_data[['text_polarity', 'title_polarity', 'site_url', 'bias']].dropna()

    # Formatting URLs

    pp_data['site_url'] = pp_data['site_url'].apply(lambda x : urlparse(x).netloc if ('https://' in x) else x)
    pp_data['site_url'] = pp_data['site_url'].apply(lambda x : urlparse(x).netloc if ('http://' in x) else x)
    pp_data['site_url'] = pp_data['site_url'].apply(lambda x : x[x.find('www.') : ] if ('www.' in x) else x)
    pp_data['site_url'] = pp_data['site_url'].apply(lambda x : x[x.find('www.') : ] if ('www.' in x) else x)
    pp_data['site_url'] = pp_data['site_url'].apply(lambda x : x[ : x.find('.')] if ('.' in x) else x)
    pp_data['site_url'] = pp_data['site_url'].apply(lambda x : x[ : x.find('.')] if ('.' in x) else x)
    pp_data['site_url'] = pp_data['site_url'].apply(lambda x : np.nan if (x == 'www') else x).dropna()
    pp_data = pp_data.rename(columns={'site_url': 'publisher'})
    # Dummy categories #
    publishers = pd.get_dummies(pp_data['publisher'])
    publishers.to_csv('publishers.csv', index=False)

    # Text polarity vectorization
    pp_data['text_polarity_bias_vneg'] = pp_data['text_polarity'].apply(lambda x : 1 if (x < -0.7) else 0)
    pp_data['text_polarity_bias_neg'] = pp_data['text_polarity'].apply(lambda x : 1 if (x >= -0.7) & (x < -0.4) else 0)
    pp_data['text_polarity_neutral_neg'] = pp_data['text_polarity'].apply(lambda x : 1 if (x >= -0.4) & (x <  -0.1) else 0)
    pp_data['text_polarity_neutral'] = pp_data['text_polarity'].apply(lambda x : 1 if (x >= -0.1) & (x <=  0.1) else 0)
    pp_data['text_polarity_neutral_pos'] = pp_data['text_polarity'].apply(lambda x : 1 if (x > 0.1) & (x <=  0.4) else 0)
    pp_data['text_polarity_bias_pos'] = pp_data['text_polarity'].apply(lambda x : 1 if (x > 0.4) & (x <= 0.7) else 0)
    pp_data['text_polarity_bias_vpos'] = pp_data['text_polarity'].apply(lambda x : 1 if (x > 0.7) else 0)
    # Title polarity vectorization
    pp_data['title_polarity_bias_vneg'] = pp_data['title_polarity'].apply(lambda x : 1 if (x < -0.7) else 0)
    pp_data['title_polarity_bias_neg'] = pp_data['title_polarity'].apply(lambda x : 1 if (x >= -0.7) & (x < -0.4) else 0)
    pp_data['title_polarity_neutral_neg'] = pp_data['title_polarity'].apply(lambda x : 1 if (x >= -0.4) & (x <  -0.1) else 0)
    pp_data['title_polarity_neutral'] = pp_data['title_polarity'].apply(lambda x : 1 if (x >= -0.1) & (x <=  0.1) else 0)
    pp_data['title_polarity_neutral_pos'] = pp_data['title_polarity'].apply(lambda x : 1 if (x > 0.1) & (x <=  0.4) else 0)
    pp_data['title_polarity_bias_pos'] = pp_data['title_polarity'].apply(lambda x : 1 if (x > 0.4) & (x <= 0.7) else 0)
    pp_data['title_polarity_bias_vpos'] = pp_data['title_polarity'].apply(lambda x : 1 if (x > 0.7) else 0)
    # Bias vectorization
    pp_data_before = pp_data['bias']
    pp_data = pp_data.drop(['text_polarity', 'title_polarity', 'publisher', 'bias'], axis=1)
    bias_data = pd.DataFrame()
    bias_data['bias'] = pp_data_before.apply(lambda x : 1 if (x == 1) else 0)
    bias_data['not_bias'] = pp_data_before.apply(lambda x : 1 if (x == 0) else 0)

    model_data = pd.concat([publishers, pp_data, bias_data], axis=1)
    model_data = model_data.sample(frac=1).reset_index(drop=True)
    model_data.to_csv('model_data.csv', index=False)

    return model_data

# Trains the model
def train(model, data, path=None):

    simple_dataset = data

    Y = simple_dataset[['bias', 'not_bias']]
    X = simple_dataset.drop(columns=['bias', 'not_bias'], axis=1)

    print (X.keys())
    print (Y.head())

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    batch_size = 30

    model.fit(x=x_train, y=y_train,
            batch_size=batch_size,
            epochs=50)

    print (model.evaluate(x=x_test, y=y_test, batch_size=batch_size))
    if path != None:
        save_model(model, filepath=path)

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



# Uncomment to reprocess the data from the sources
# pre_process_data()

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

pp_data = loadAndPrepare()

print (pp_data.shape)
train(model, pp_data, 'deep_net_config_1.hdf5')
#model = load_model('deep_net_config_1.hdf5')
print (predict(model, 'U.S. Has Highest Share of Foreign-Born Since 1910, With More Coming From Asia', 'The foreign-born population in the United States has reached its highest share since 1910, according to government data released Thursday, and the new arrivals are more likely to come from Asia and to have college degrees than those who arrived in past decades.', 'other'))
