import pandas as pd
import tweepy
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
		
