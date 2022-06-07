import pandas as pd
import tweepy
from datetime import datetime

from sklearn.model_selection import train_test_split
from config import consumer_key, consumer_secret, access_token_key, access_token_secret

def init_api():
	#API config:
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, secure=True)
	auth.set_access_token(access_token_key, access_token_secret)

	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	
	return api


def import_tweets(account, api, number_tweets=300):
	# This function scraps the last 300 tweets from account
	# and then returns all tweets excluding ReTweets
	tweets = []
	
	try:
		raw_tweets = tweepy.Cursor(api.user_timeline, id=account[1:], tweet_mode="extended").items(number_tweets)
		for tweet in raw_tweets:
			text_tweet = tweet.full_text
			if not("RT @" in text_tweet):   #We exculde RTs
				tweets.append(text_tweet.lower())
		return tweets

	except:
		return 0
		

def validadtion_split(X, val_size=0.2, random_state=666):
	# Splits data in train/test and validation
	X_t, X_val = train_test_split(X, val_size, random_state=random_state)

	return X_t, X_val
	

def import_tweets_from_list(acc_list, n_of_tweets=300, max_time=3600):
	api = init_api()
	remaining = acc_list
	all_tweets = dict()
	
	tic = datetime.now() 
	toc = lambda: (datetime.now() - ini).total_seconds()
	
	while(remaining != [] and toc()<max_time):
    	for acc in remaining:
        	tweets_from_acc = import_tweets(acc, api, n_of_tweets)
    
        	if(tweets_from_acc == 0):
            	print("ERROR: " + acc)
        	else:
            	all_tweets[acc] = tweets_from_acc
            	remaining.remove(acc)
    print('Elapsed in', toc()/60, 's')
    
    return all_tweets, remaining


