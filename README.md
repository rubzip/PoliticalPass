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
- [ ] Subir como otro proyeco a github la version buena sin las APIs
- [ ] wordcloud
- [ ] ordenar por carpetas
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

I have selected some relevant political profiles in Spain (politicians, tweetstars, youtubers, ...), labeled as 0 (rigthts) and 1 (leftist), then I have downloaded the n last tweets from each user labeled based on who wrote it. 

### Problems
 * Nowadays left-wing and right-wing concepts are senseless since we have 2 variables in [political spectrum](https://en.wikipedia.org/wiki/Political_spectrum), but it was the simplest way to label data. For example I have clasified [Juan Ramón Rallo](https://es.wikipedia.org/wiki/Juan_Ramón_Rallo) (liberal) as rightist.
 * Another problem of data is that we have a large amount of tweets from a small quantity of accounts, it could be problematic. For example: supose that we have a leftist huge fan of basketball and he is the unique person that tweets about basket in dataset, if we evaluate in our model another basketaball fan or even a basketball player, possibly the result would be leftist.


## Mining

Using `Tweepy` we downnload the `number_tweets` last tweets from `at` user:

```python
def import_tweets(at, number_tweets=300):
#https://stackoverflow.com/questions/30359801/how-to-successfully-get-all-the-tweets-for-one-user-with-tweepy
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

## Spacy or NLTK?

Before I started this projet I never have listened about NLP. I decided to use Spacy beacuse in NLTK doesn't exist any lemmatizer in spanish. 

## Cleaning

As I said I used Sapcy:



https://towardsdatascience.com/email-spam-detection-1-2-b0e06a5c0472

https://likegeeks.com/es/tutorial-de-nlp-con-python-nltk/#Implementaciones_del_NLP
RNN

## Requeriments
 * python3
 * tweetpy
 * NLKT
