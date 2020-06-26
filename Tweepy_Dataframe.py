# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 22:47:19 2020

@author: Shraddha
"""

import Token_credential
import numpy as np
import pandas as pd
import tweepy as tw

from tweepy import OAuthHandler # authenticate based on the token credential
from tweepy import API

class TwitterAuthenticator(): # class for authentiction
    
    def authenticate_tweet(self): #function for authentication
        auth = OAuthHandler(Token_credential.CONSUMER_KEY, Token_credential.CONSUMER_KEY_SECRET) #authenticaing our credentials
        auth.set_access_token(Token_credential.ACCESS_TOKEN,Token_credential.ACCESS_TOKEN_SECRET)
        return auth
    
class TwitterClient():  #access user data
    
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_tweet()
        self.twitterclient = API(self.auth, wait_on_rate_limit = True)
        
    def get_twitter_api(self):
        return self.twitterclient 

class TweetAnalyzer():
    
    def tweet_to_dataframe(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['location'] = np.array([tweet.geo for tweet in tweets])
        #print(tweets)
        return df
        
        
if __name__ == "__main__": # calling main class
    twitterclient = TwitterClient()
    api = twitterclient.get_twitter_api()
    tweetanalyzer = TweetAnalyzer()
    tweets = tw.Cursor(api.search, q = ['#fire'],lang = 'en', since = '2020-03-10').items(1000)
    tweets_details = [[tweet.text, tweet.geo, tweet.user.location]for tweet in tweets]
    df = pd.DataFrame(data = tweets_details, columns = ['text','geo','location'])
    df.to_csv('fire.csv')
    #tweets = api.search(q = ['corona','pandemic'], lang = "en", count = 2000)    #bulit in function in api
    #print(tweets[0])
    #df = tweetanalyzer.tweet_to_dataframe(tweets)
    #df.to_csv('result.csv')
    #print(df.head(10))