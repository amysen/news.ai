import pandas as pd
import numpy as np
import pickle
import model

from sklearn import cross_validation, datasets, tree, preprocessing
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn import metrics
import Function_File as files

from flask import Flask, request

"""
    To run a flask server just type into your terminal

    FLASK_APP=app.py
    flask run
    
"""

app = Flask(__name__)                                       

def prediction(info):
    train_model = model.get_model()
    prediction = model.predict(train_model,info['title'],info['text'], info['publisher'])
    return prediction
@app.route("/predict", methods=["POST"])                    # YOU CAN CHANGE THIS TO SUIT YOUR METHODS
def predict():
    inputUrl = request.data
    info = files.getArticleData(inputUrl)
    return prediction(info)                                    # I then returned the prediction which the model fucntion did for me

if __name__ == '__main__':
    app.run(debug=True)
