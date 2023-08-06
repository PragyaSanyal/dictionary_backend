from flask import Flask
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re
app=Flask(__name__)


@app.route('/')
@app.route('/<string:word>')
def get_all_data(word=' '):
    meaning,synonyms,antonyms,sentences= [],[],[],[]

    url1 = "https://www.yourdictionary.com/{}".format(word)
    url2 = "https://thesaurus.yourdictionary.com/{}".format(word)
    url3 = "https://sentence.yourdictionary.com/{}".format(word)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    webpage1 = requests.get(url1, headers=headers).text
    soup1 = bs(webpage1, 'lxml')
    for i in soup1.find_all('div', class_='definition-cluster'):
        meaning.append(i.text)

    webpage2 = requests.get(url2, headers=headers).text
    soup2 = bs(webpage2, 'lxml')
    result = soup2.find_all('div', class_='mt-3')
    for i in result:
        for j in i.find_all('li'):
            synonyms.append(j.text)
    synonyms = list(set(synonyms))
    result = soup2.find_all('div', class_="mt-4")
    for i in result:
        for j in i.find_all('li'):
            antonyms.append(j.text)
    antonyms = list(set(antonyms))

    webpage3 = requests.get(url3, headers=headers).text
    soup3 = bs(webpage3, 'lxml')
    for i in soup3.find_all('div', class_="sentence-item__wrapper"):
        sentences.append(i.text)


    return {
        'word':word,
        'meanings':meaning,
        'synonyms':synonyms,
        'antonyms':antonyms,
        'sentences':sentences
    }












if __name__ == '__main__':
    app.run(debug=True)

