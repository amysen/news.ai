from newspaper import Article
import datetime
import json

# sudo pip install python-dateutil --upgrade


def xzyggy():

    # empty function for later stuff for page.py pages you might need

    return bias_categories


def getArticleData(inputURL):

	article = Article(inputURL)

	article.download()
	article.parse()

	article.nlp()

	domain = inputURL.split('//')[-1].split('/')[0]

	articleDict = {'full_url': inputURL,'domain': domain, 'authors': article.authors, 'title': article.title, 'text': article.text, 'top_image': article.top_image, 'keywords': article.keywords, 'summary': article.summary}

	return articleDict


def getDomainData(inputDomain):
	json_data=open('bias.json')
	jdata = json.load(json_data)

	if (inputDomain[:4] == 'www.'):
		inputDomain = inputDomain[4:]


	result = jdata.get(inputDomain)


	if result is None:
		inputDomain = inputDomain.replace(".co.uk",".com")
		result = jdata.get(inputDomain)

	json_data.close()

	return result


def getDomainBias(inputBias):
	json_data=open('bias_description.json');
	jdata = json.load(json_data)
	
	biasDesc = jdata.get(inputBias)

	json_data.close()

	return biasDesc

    
    