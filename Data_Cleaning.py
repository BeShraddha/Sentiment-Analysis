# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:00:06 2020

@author: Shraddha
"""

import pandas as pd
import numpy as np
import re
from textblob import TextBlob   #method to analyze sentiment of a given text
import matplotlib.pyplot as plt
from glob import glob

class DataCleaning():
    def clean_tweet(self, tweet):  #for cleaning the data or removing regular expression and hyperlinks
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):   #sentiment analysis upon cleaned data
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
        
    def loc_count(self, location):
        pass
        
    def PlotPieChart(self, positive, negative, neutral):   #plotting pie chart
        labels = ['Positive [' + str(positive) + ']', 'Neutral [' + str(neutral) + ']','Negative [' + str(negative) + ']']
        sizes = [positive, neutral, negative]
        colors = ['green','red','blue']
        plt.pie(sizes, colors=colors, labels = labels, startangle=90, autopct='%.1f%%')
        plt.title('How people are reacting on disaster by analyzing '+str(len(df['sentiment']))+' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
       
    
    def BarPlotLocation(self, df1):
        loc_count = {}
        for location in df1:
            loc_count[location] = 0
        for location in df1:
            loc_count[location] += 1
        
        loc = {}
        for i,j in loc_count.items():
            if j > 50:
                loc[i]=j
        key = loc.keys()
        value = loc.values()
        
        plt.figure(figsize=(20,10))
        index = np.arange(len(key))
        plt.bar(key, value)
        plt.xlabel('Location', fontsize=15)
        plt.ylabel('No of Count', fontsize=15)
        plt.xticks(index, key, fontsize=10, rotation=30)
        plt.title('Disaster affected area')
        plt.show()

if __name__ == "__main__": # calling main class
    #extracting multiple csv file 
    filenames = glob("*.csv")
    df = []
    for filename in filenames:
        lf = pd.read_csv(filename, index_col=None, header=0)
        df.append(lf)

    # Concatenate all data into one DataFrame
    df = pd.concat(df, ignore_index = True, sort = True)
    datacleaning = DataCleaning()
    df['sentiment'] = np.array([datacleaning.analyze_sentiment(tweet) for tweet in df['text']])
    
    #getting location wise bar plot
    df1 = df['location'].dropna()
    datacleaning.BarPlotLocation(df1)
    
    #API.geo_id(id)
    df.to_csv('result.csv')  
    
    positive, negative, neutral = 0, 0, 0
    for senti in df['sentiment']:
        if senti == 1:
            positive += 1
        elif senti == 0:
            neutral += 1
        else:
            negative += 1
    
    datacleaning.PlotPieChart(positive, negative, neutral)
    