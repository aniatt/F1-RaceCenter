import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# TODO
# 1. Gather more accurate headline data for Sentiment Analysis: Driver Statements, Team Statements

def getHeadlines(driverName):
    translateDict = {
        'MAX VERSTAPPEN': 'max-verstappen',
        'SERGIO PEREZ': 'sergio-perez',
        'CHARLES LECLERC': 'charles-leclerc',
        'CARLOS SAINZ': 'carlos-sainz',
        'LEWIS HAMILTON': 'lewis-hamilton',
        'GEORGE RUSSELL': 'george-russell',
        'LANDO NORRIS': 'lando-norris',
        'DANIEL RICCIARDO': 'daniel-ricciardo',
        'ESTEBAN OCON': 'esteban-ocon',
        'FERNANDO ALONSO': 'fernando-alonso',
        'LANCE STROLL': 'lance-stroll',
        'SEBASTIAN VETTEL': 'sebastian-vettel',
        'VALTTERI BOTTAS': 'valtteri-bottas',
        'GUANYU ZHOU': 'guanyu-zhou',
        'PIERRE GASLY': 'pierre-gasly',
        'YUKI TSUNODA': 'yuki-tsunoda',
        'ALEXANDER ALBON': 'alexander-albon',
        'NICHOLAS LATIFI': 'nicholas-latifi',
        'KEVIN MAGNUSSEN': 'kevin-magnussen',
        'MICK SCHUMACHER': 'mick-schumacher',
    }
    
    url = 'https://www.formula1.com/en/drivers/'+ translateDict[driverName] +'.html'
    
    try:
        response = requests.get(url)
        content = response.content
    except:
        content = ' '

    soup = BeautifulSoup(content.decode('utf-8','ignore'), 'html.parser')
    scrapedArticles = soup.find_all('h4', attrs={'class':'teaser-info-title'})
    
    return scrapedArticles


def sentimentAnalysis(df):
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()

    driverSentiment = pd.DataFrame(columns = ['Sentiment'])
    data = {column: [] for column in driverSentiment}
    for driver in df['Predicted Finish']:
        headlines = getHeadlines(driver)
        cnt = 0
        avgScore = 0
        for i in range(len(headlines)):
            avgScore += sid.polarity_scores(headlines[i].text)['compound']
            cnt += 1
        
        try:
            avgScore /= cnt
        except:
            avgScore = 0
        data['Sentiment'].append(avgScore)
    
    driverSentiment = pd.DataFrame(data)
    return driverSentiment