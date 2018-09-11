from newspaper import Article
import datetime
import json

# sudo pip install python-dateutil --upgrade
bias_categories = ["right", "right-center", "left", "leftcenter", "center", "fake-news", "pro-science", "satire", "conspiracy"]


def xzyggy():

    # empty function for later stuff for page.py pages you might need

    return bias_categories


def getArticleData(inputURL):

	article = Article(inputURL)

	article.download()
	article.parse()

	article.nlp()

	domain = inputURL.split('//')[-1].split('/')[0]

	articleDict = {'full_url': inputURL,'domian': domain, 'authors': article.authors, 'title': article.title, 'text': article.text, 'top_image': article.top_image, 'keywords': article.keywords, 'summary': article.summary}

	return articleDict

    
    