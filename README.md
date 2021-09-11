# PoliticalPass

Deep Learning project. The objetive is to predict if a (spanish) twitter account is left-wing or right-wing based on most often tweeted words.

The most important files are:

* `config.py` : Python file that stores API keys.

* `datos.csv` : Info about all users analayzed.

* `data_mining.ipynb` : Download the `number_tweets` last tweets from each user. Tweets are stored in `raw_tweets.csv`.  

* `data_cleaning.ipynb` : Tokenizes and cleans stopwords.

* `create_dictionary.ipynb` : Creates a dictionary formed by the `n_max` most frequent words.

* `transform_data.ipynb` : It takes the tokenized tweets from `data_cleaning.ipynb` and labels data aplying the dictionary `dictionary.json`. After runing this notebook, we have correctly formated our data as `X` (numpy array, variable lengths) and `y` (0 or 1). 

* `model.ipynb` : Our model.

## To do list (Only for me)
- [ ] Implement recurrency on data mining.
- [ ] Optimize lemmatizing.
- [ ] Build another list of twiter personalities to test the NN wuth a different datasent (almost 18 accounts).

## Requirements
This project uses the following Python libraries

* `Tweepy` : To download tweets.
* `spaCy` : Used to tokenize words and lemmatize.
* `es_dep_news_trf` : Spanish transformer pipeline.
* `wordcloud` : Used to create word clouds from dictionaries.

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

### Data cleaning
The process was easy, first of all tokenize, filter wordclouds and lemmatization.

I found some problems with spacy stopwords, resulting the most often words:
![WordCloud Bad](https://github.com/rubzip/PoliticalPass/blob/main/wordcloud_bad.png)
I fitered:
```python
delete = {
    'a', 'y', 'o', 'of', 'in', 'i', 'to', 'e', 'm', 'and', 'the'
}

dictionary_2 = dictionary
for i in delete:
    dictionary_2[i] = 0
```

Result of most often words (correctly cleaned):
![WordCloud](https://github.com/rubzip/PoliticalPass/blob/main/wordcloud.png)

### Data label
I created a dictionary using the 2000 most often words, after that every exaple is labeled as X: a numpy array of variable length (minimum 3 words), every element in the array is a number between 0 and 1999. Y is 0. or 1. depending on the tweet is left-wing or not. 

## Model
The model implemented is a [Recursive Neural Network (RNN)](https://en.wikipedia.org/wiki/Recursive_neural_network).

### Data split
I have applied one_hot_encoding . Using `model_selection` from `sklearn` I have splitted our 38423 examples as 80% training set and 20% test set.


https://towardsdatascience.com/email-spam-detection-1-2-b0e06a5c0472

https://likegeeks.com/es/tutorial-de-nlp-con-python-nltk/#Implementaciones_del_NLP
RNN
