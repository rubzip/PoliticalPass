# PoliticalPass

The goal of this project is to predict if a (Spanish) twitter personality is left-wing or right-wing based on his tweets.

The most important files are:

* `config.py` : Python file that stores API keys.

* `datos.csv` : Info about all users analyzed.

* `data_mining.ipynb` : Downloads the `number_tweets` last tweets from each user. Tweets are stored in `raw_tweets.csv`.  

* `data_cleaning.ipynb` : Tokenizes and cleans stopwords.

* `create_dictionary.ipynb` : Creates a dictionary formed by the `n_max` most frequent words.

* `transform_data.ipynb` : It takes the tokenized tweets from `data_cleaning.ipynb` and labels data applying the dictionary `dictionary.json`. After running this notebook, we have correctly formatted our data as `X` (numpy array, variable lengths) and `y` (0 or 1). 

* `model.ipynb` : 

## To do list (Only for me)
- [ ] **Build the model.** A good idea could train a pre-trained model as [BERT](https://www.tensorflow.org/text/tutorials/fine_tune_bert). 
- [ ] Increment the dataset.
- [ ] Divide dataset in Train/Dev/Test. Train and Test must have the same data origin, Test must have different Twitter accounts
- [ ] Create an embedding projector: https://projector.tensorflow.org/
- [ ] Organize better the cleaning directory, we have a lot of useless files.
- [ ] Implement recurrency on data mining.
- [ ] Optimize lemmatizing.
- [ ] Build another list of Twitter personalities to test the NN with a different dataset (almost 18 accounts).
- [ ] Program a web interface that scraps tweets and uses the model to predict the political ideology.
- [ ] Upload the trained model to hugging face.
- [ ] Google Form.
- [ ] Fix `.gitnore` to ignore the `config.py` file. 

## Requirements
This project uses the following Python libraries

* `Tweepy` : To download tweets.
* `spaCy` : Used to tokenize words and lemmatize.
* `es_dep_news_trf` : Spanish transformer pipeline.
* `wordcloud` : Used to create word clouds from dictionaries.
* `TensorFlow`

## About data
I have selected some relevant political profiles in Spain (`datos.csv`), labeled as 0 (rightist) and 1 (leftist), then I have downloaded the N last tweets from them. 

### Twitter Profiles

### Train/Test/Validation Split
First of all I have randomly splitted our twitter accounts in 2 groups train/test - validation (80% - 20%). I have built the data dictionary and trained the model only with the twitter accounts that belong to the first group.

### Do you feel incomplete the dataset?
It's really hard to make a dataset that represents correctly the political Spanish spectrum, I would appreciate any sugestions. If you want to help with the dataset, please make a pull request with `datos.csv` updated or fill this Google form().

### Possible problems
 * Nowadays left-wing and right-wing concepts are senseless since we have 2 variables in [political spectrum](https://en.wikipedia.org/wiki/The_Political_Compass), but it was the simplest way to label data. 
 * Another problem of data is that we have a large amount of tweets from a small quantity of accounts, this could be problematic (or not).


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


## Data Cleaning

### Spacy or NLTK?
Before I started this projet I never have listened about NLP. I decided to use `Spacy` beacuse in NLTK library doesn't exist any lemmatizer in spanish. Concretely I have loaded `'es_dep_news_trf'`.

### Tokenization

Result of most often words (correctly cleaned):
![WordCloud](https://github.com/rubzip/PoliticalPass/blob/main/wordcloud.png)

### Word Embedding

### Word filtering
The process was easy, first of all tokenize, filter wordclouds, and lemmatization.

I found some problems with spacy stopwords, resulting the most often words:
![WordCloud Bad](https://github.com/rubzip/PoliticalPass/blob/main/wordcloud_bad.png)
I filtered:
```python
delete = {
    'a', 'y', 'o', 'of', 'in', 'i', 'to', 'e', 'm', 'and', 'the'
}

dictionary_2 = dictionary
for i in delete:
    dictionary_2[i] = 0
```



### Data label
I created a dictionary using the 2000 most often words, after that every example is labeled as X: a numpy array of variable length (minimum 3 words), and every element in the array is a number between 0 and 1999. Y is 0. or 1. depending on whether the tweet belongs to a left-wing personality or not. 

## Model
The model implemented is a [Recursive Neural Network (RNN)](https://en.wikipedia.org/wiki/Recursive_neural_network).

### Data split
I have applied one_hot_encoding. Using `model_selection` from `sklearn` I have split our 38423 examples as 80% training set and 20% test set.
We should divide tweets by users.
