import pandas as pd
import tweepy
from datetime import datetime

from sklearn.model_selection import train_test_split
from config import consumer_key, consumer_secret, access_token_key, access_token_secret

def init_api():
	#API config:
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token_key, access_token_secret)

	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	
	return api

def validation_split(df, val_size=0.2, random_state=666):
	# Splits data in train/test and validation
	df_t, df_val = train_test_split(df, test_size=val_size, random_state=random_state)

	return df_t.sort_index(), df_val.sort_index()

def balanced_split(df, column='Izda', val_size=0.2, random_state=666):
	# Takes the same amount for 0 and 1
	df_t0, df_val0 = validation_split(df[df[column]==0], val_size, random_state)
	df_t1, df_val1 = validation_split(df[df[column]==1])
	# Concat of both DataFrames:
	df_t = pd.concat([df_t1, df_t0])
	df_v = pd.concat([df_val1, df_val0])

	return df_t, df_v


def list_to_csv(tweets, classification, root):
	# Converts the list-like tweets into a CSV stored in root
	data_to_csv = []
	
	accounts = tweets.keys()
	for acc in accounts:
		left = classification[acc]
		for tweet in tweets[acc]:
			data_to_csv.append( (acc, tweet, left) )

	colunms = ['User', 'Tweet', 'Left']
	df = pd.DataFrame(data_to_csv, columns=colunms)

	df.to_csv(root, index=False)
	
	return df

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
	

def import_tweets_from_list(acc_list, n_of_tweets=300, max_time=3600, max_iter=10):
	# Takes a list of Twitter accounts and downloads the last n_of_tweets tweets
	api = init_api()
	remaining = acc_list
	all_tweets = dict()
	
	tic = datetime.now() 
	toc = lambda: (datetime.now() - tic).total_seconds()
	
	i = 0
	while(remaining != [] and toc()<max_time and i<max_iter):
		i += 1
		for acc in remaining:
			tweets_from_acc = import_tweets(acc, api, n_of_tweets)

			if(tweets_from_acc == 0):
				print("ERROR: ", acc)
			else:
				all_tweets[acc] = tweets_from_acc
				print('Completed: ', acc)
				remaining.remove(acc)

	print('Elapsed in', toc()/60, 'min')
	
	return all_tweets, remaining
