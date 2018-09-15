# -*- coding: utf-8 -*-

import json

from flask import Flask, request, jsonify, session, escape, redirect, abort
from flask.helpers import url_for
from flask.templating import render_template

from Function_File import *
from Analytics import *


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def loadHome():
    try:
        if request.method == "POST":
            return render_template('home.html')
        else:
            return render_template('home.html')
    except Exception as e:
        print("Error in homepage:", e)
        traceback.print_exc()
        if request.method == "POST":
            return jsonify({'error':500})
        abort(500)


@app.route("/analytics", methods=["POST", "GET"])
def analyticsPage():
    try:
        if request.method == "POST":
            print('posting to analyticsPage in main.py')

            url = request.data
            url = url.decode('utf-8')
            url = json.loads(url)
            url = url['url']
            
            data = getArticleData(url)
            # prediction = kikosmodel(domain, text, title); 
            print('DATA: ', data)

            domain = data['domain']

            bias = getDomainData(domain)
            print('BIAS: ', bias)
            
            if bias == None:
                combinedData = {'articleData': data, 'biasData': bias}
            else:
                biasVal = bias['bias']
                biasDesc = getDomainBias(biasVal)
                combinedData = {'articleData': data, 'biasData': bias, 'biasDesc': biasDesc}

            print('COMBINED DATA: ', combinedData)
            combinedData = json.dumps(combinedData)

            return combinedData
        else:
            return render_template("analytics.html")

    except Exception as e:
        print("Error in analytics page:", e)
        traceback.print_exc()
        if request.method == "POST":
            return jsonify({'error':500})
        abort(500)


@app.route("/trending", methods=["GET", "POST"])
def trendingPage():
    
    try:
        if request.method == "POST":
            trending = googleTrending()

            trending = json.dumps(trending)
            return trending

        # if request.method == "GET":
        #     print('IN GET')
        #     trending = googleTrending()

        #     trending = json.dumps(trending)

        #     return render_template("trending.html")

        else:
            return render_template("trending.html")

    except Exception as e:
        print("Error in trending page:", e)
        traceback.print_exc()
        if request.method == "POST":
            return jsonify({'error':500})
        abort(500)


# @app.route("/history", methods=["GET", "POST"])
# def historyPage():
#     try:
#         if request.method == "POST":

#         else:
#             return render_template("trending.html")

#     except Exception as e:
#         print("Error in trending page:", e)
#         traceback.print_exc()
#         if request.method == "POST":
#             return jsonify({'error':500})
#         abort(500)






#    KEYGEN FUNCTIONS
def createNewKey():
    return os.urandom(64)

def refreshKey():
    #print("REFRESHING KEY...")
    app.secret_key = createNewKey()

app.secret_key = "a"

if __name__ == "__main__":
	app.debug=True
	app.run(host="0.0.0.0", port=80)

