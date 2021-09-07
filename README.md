# PoliticalPass

Deep Learning project. The objetive is to predict if a (spanish) twitter account is left-wing or right-wing based on most often tweetted words.

The most important files are:

* `config.py` : Python file that stores API keys.

* `datos.csv` : Info about all users analayzed.

* `data_mining.ipynb` : Download the `number_tweets` last tweets from each user. Tweets are stored in `raw_tweets.csv`.  

* `data_cleaning.ipynb` : 


## TAREAS (Only for me)
- [x] Añadir un .gitnore https://medium.com/black-tech-diva/hide-your-api-keys-7635e181a06c
- [ ] Implemetar manera de minar data de manera paralela
- [ ] Limpiar los datos
- [ ] Crear diccionario de palabras
- [ ] Aumentar el dataset (más cuentas y más twits)
- [x] Subir como otro proyeco a github la version buena sin las APIs
- [ ] wordcloud
- [x] ordenar por carpetas
- [ ] añadir mas graficas, balanceo de datos

## Requirements

This project uses the following Python libraries

* `Tweepy` : To download tweets.
* `spaCy` : Used to tokenize words and lemmatize.
* spcay...
* `wordcloud` : Used to create word clouds with the article text.

After installing the `spaCy` library you must install a language model to be able to tokenize the article.

For `Spanish` you can run this one:

`python -m spacy download es_core_news_sm`

For other languages please check the following link: https://spacy.io/usage/models

## About data
I have selected some relevant political profiles in Spain (`datos.csv`), labeled as 0 (rightist) and 1 (leftist), then I have downloaded the n last tweets from each user labeled based on who wrote it. 

### Problems
 * Nowadays left-wing and right-wing concepts are senseless since we have 2 variables in [political spectrum](https://en.wikipedia.org/wiki/Political_spectrum), but it was the simplest way to label data. 
 * Another problem of data is that we have a large amount of tweets from a small quantity of accounts, this could be problematic.


## Mining

Using `Tweepy` we downnload the `number_tweets` last tweets from `at` user:

```python
def import_tweets(at, number_tweets=300):
	#API config:
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token_key, access_token_secret)

	api = tweepy.API(auth)

	#tweets are stored in a list
	tweets = []

	try:
		raw_tweets = tweepy.Cursor(api.user_timeline,id=at[1:], tweet_mode="extended").items(number_tweets)
		for tweet in raw_tweets:
			text_tweet = tweet.full_text
			if not("RT @" in text_tweet):   #We exculde RTs
				tweets.append(text_tweet)

		return(tweets)

	except:
		return(0)
```


## Cleaning

### Spacy or NLTK?

Before I started this projet I never have listened about NLP. I decided to use `Spacy` beacuse in NLTK doesn't exist any lemmatizer in spanish. 
I loaded `'es_dep_news_trf'`, maybe a bad decision because is one of the most heavier files.

The process was easy, first of all tokenize, filter wordclouds and lemmatization.

I found some problems with spacy stopwords, resultind the most often words:
![WordCloud Bad](https://github.com/rubzip/PoliticalPass/blob/main/wordcloud_bad.png)

Result of most often words (correctly cleaned):
![WordCloud](https://github.com/rubzip/PoliticalPass/blob/main/wordcloud.png)


https://towardsdatascience.com/email-spam-detection-1-2-b0e06a5c0472

https://likegeeks.com/es/tutorial-de-nlp-con-python-nltk/#Implementaciones_del_NLP
RNN

