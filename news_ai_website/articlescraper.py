from newspaper import Article

def getArticleData(inputURL):

	article = Article(inputURL)

	article.download()
	article.parse()

	article.nlp()

	domain = inputURL.split(“//”)[-1].split(“/”)[0]

	articleDict = {'domian': domain, 'authors': article.authors, 'title': article.title, 'text': article.text, 'top_image': article.top_image, 'keywords': article.keywords, 'summary': article.summary}
	print(articleDict)

	return articleDict
