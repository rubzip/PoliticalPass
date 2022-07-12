# PoliticalPass

The goal of this project is to predict if a (Spanish) twitter personality is left-wing or right-wing based on his tweets.

## 0. About data
I have selected some relevant political profiles in Spain (`ALL_twitter_accounts.csv`), labeled as 0 (rightist) and 1 (leftist), then I have downloaded the N last tweets from them. 

### Twitter Profiles

### Train/Test/Validation Split
First of all I have randomly splitted our twitter accounts in 2 groups train/test - validation (80% - 20%). The tokenizer data comes from the train/test dataset.

### Do you feel incomplete the dataset?
It's really hard to make a dataset that represents correctly the political Spanish spectrum, I would appreciate any sugestions. If you want to help with the dataset, please make a pull request with `ALL_twitter_accounts.csv` updated.

### Possible problems
 * Nowadays left-wing and right-wing concepts are senseless since we have 2 variables (or maybe more) in the [political spectrum](https://en.wikipedia.org/wiki/The_Political_Compass), but it was the simplest way to label data. 
 * Another problem of data is that we have a large amount of tweets from a small quantity of accounts, this could be problematic (or not).


## 1. Mining
Using `Tweepy` and Twitter's API (`config.py`), I have downloaded the last 300 tweets from every user:

```python
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
```
Resulting raw tweets were stored as a .csv in `./0_DATA/train-test_tweets.csv` and `./0_DATA/val_tweets.csv`.

## 2. Cleaning

### Spacy or NLTK?
Before I started this projet I never have listened about NLP. I decided to use `Spacy` beacuse in NLTK library doesn't exist any lemmatizer in spanish. Concretely I have loaded `'es_dep_news_trf'`.

### Lemmatization of Train-Test dataset

Using the lemmatizer `'es_dep_news_trf'` from `Spacy` (`nlp`), I have lemmatized all tweets from `./0_DATA/train-test_tweets.csv` and stored in `./0_DATA/train-test_lemma.csv`.

```python
new_tweets = df_train['Tweet'].map(lambda x: lemmatize_tweet(nlp, x))
```

```python
def lemmatize_tweet(nlp, tweet):
    #This function takes a tweet as a spacy.doc and returs the tweet lemmatized
    
    #Some extra stopwords:
    delete = {
        'a', 'of', 'in', 'i', 'to', 'e', 'm', 'and', 'the'
    }
    new_tweet = ''
    
    #In the next step we are going to remove stop words and lemmatize
    for token in nlp(tweet):
        if (token.text.isalpha() and not(token.is_stop or token.lemma_ in delete)):#We are going to remove not alphanumeric tokens and stopwords
            new_tweet += ' ' + token.lemma_
    
    #We return tweet tokenized and lemmatized as a tuple: 
    return new_tweet
```

### Tokenization

Taking the lemmatized tweets (train-test), I have created the tokenizer (5000 words):

```python
# Creation and fitting of the Tokenizer:
tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
tokenizer.fit_on_texts(new_tweets)
```
Result of most often words:
![WordCloud](https://github.com/rubzip/PoliticalPass/blob/main/4_IMAGES/wordcloud.png)

### Lemmatization of validation dataset
Also it has been lemmatized all tweets from `./0_DATA/val_tweets.csv`, and the result has been stored in `./0_DATA/val_lemma.csv`.


## 3. Model
Working... 
The main idea now is to use ULMFIT structure:

https://www.analyticsvidhya.com/blog/2018/11/tutorial-text-classification-ulmfit-fastai-library/?utm_source=blog&utm_medium=top-pretrained-models-nlp-article

https://arxiv.org/abs/1801.06146

## To do list (Only for me)
- [ ] **Build the model.** A good idea could train a pre-trained model as [BERT](https://www.tensorflow.org/text/tutorials/fine_tune_bert). 
- [ ] Increment the dataset.
- [ ] Create an embedding projector: https://projector.tensorflow.org/
- [ ] Program a web interface that scraps tweets and uses the model to predict the political ideology.
- [ ] Upload the trained model to hugging face.
- [ ] Fix `.gitnore` to ignore the `config.py` file. 

The most important files are:

* `./ALL_twitter_accounts.csv` : Info about all users analyzed.

* `./1_MINING/config.py` : Python file that stores API keys.
* `./1_MINING/data_mining.ipynb` : Makes the train-test/val split and downloads the tweets.

* `./2_CLEANING/data_cleaning.ipynb` : Lemmatizes all tweets and creates the tokenizer.

* `./3_MODEL/model.ipynb` : 


## Requirements
This project uses the following Python libraries

* `Tweepy` : To download tweets.
* `spaCy` : Used to tokenize words and lemmatize.
* `es_dep_news_trf` : Spanish transformer pipeline.
* `wordcloud` : Used to create word clouds from dictionaries.
* `TensorFlow`
