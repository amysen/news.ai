import pandas as pd
import os
import project


def join_csv_files(path):
    dirs = os.listdir(path)
    df = pd.DataFrame()
    for dir in dirs:
        reuters = path + dir + '/reuters.csv'
        ny = path + dir + '/nytimes.csv'
        df = pd.concat([df, pd.read_csv(reuters), pd.read_csv(ny)])
    return df

def clean():
    data = join_csv_files('csvdataset/').sample(frac=1).reset_index()
    data = data.sample(5000).reset_index()
    print len(data)
    data = data[['KEYWORDS', 'TEXT', 'TITLE', 'URL']]
    data = data.rename(columns={'KEYWORDS':'keywords', 'TEXT':'text', 'TITLE':'title', 'URL':'site_url'})
    data = project.applyFunctions(data, 'text')
    data = project.applyFunctions(data, 'title')
    data = project.tokenizeTexts(data, 'text')
    data = project.tokenizeTitles(data, 'title')
    data['text_polarity'] = project.analyseData(data, name='text').dropna()
    data['title_polarity'] = project.analyseData(data, name='title').dropna()
    data['bias'] = 0
    data['site_url'] = data['site_url'].apply(lambda x : x[x.find('reuters') : x.find('reuters') + len('reuters')] if ('reuters' in x) else x)
    data['site_url'] = data['site_url'].apply(lambda x : x[x.find('nytimes') : x.find('nytimes') + len('nytimes')] if ('nytimes' in x) else x)
    data.to_csv('unbiasedData.csv', index=False)

clean()
