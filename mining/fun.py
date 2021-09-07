import pandas as pd
import tweepy
from config import consumer_key, consumer_secret, access_token_key, access_token_secret

#Takes at direction and returns 300 (by default) last tweets as a list
#if there is some error, returns 0
def import_tweets(at, number_tweets=300):
#https://stackoverflow.com/questions/30359801/how-to-successfully-get-all-the-tweets-for-one-user-with-tweepy
	#API config:
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, secure=True)
	auth.set_access_token(access_token_key, access_token_secret)

	api = tweepy.API(auth)

	#tweets are stored in a list
	tweets = []

	try:
		raw_tweets = tweepy.Cursor(api.user_timeline,id=at[1:], tweet_mode="extended").items(number_tweets)
		for tweet in raw_tweets:
			text_tweet = tweet.full_text
			if not("RT @" in text_tweet):   #We exculde RTs
				tweets.append(text_tweet.lower())

		return(tweets)

	except:
		return(0)
		
