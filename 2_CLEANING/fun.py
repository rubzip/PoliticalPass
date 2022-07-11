from datetime import datetime
import json
import io
from tensorflow.keras.preprocessing.text import tokenizer_from_json

def lemmatize_tweet(nlp, tweet):
    #This function takes a tweet as a spacy.doc and returs the tweet tokenized
    #and with all stopwords filtered as a str
    #Some extra stopwords:
    delete = {
        'a', 'of', 'in', 'i', 'to', 'e', 'm', 'and', 'the'
    }
    new_tweet = ''
    
    #In the next step we are going to remove stop words
    #and lemmatize words
    for token in nlp(tweet):
        if (token.text.isalpha() and not(token.is_stop or token.lemma_ in delete)):#We are going to remove not alphanumeric tokens and stopwords
            new_tweet += ' ' + token.lemma_
    
    #We return tweet tokenized and lemmatized as a tuple: 
    return new_tweet

def save_tokenizer(tokenizer, filename='./tokenizer.json'):
    #This function takes a tokenizer and get saved
    tokenizer_json = tokenizer.to_json()
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(tokenizer_json, ensure_ascii=False))
        print('Correctly saved :)')
    
def load_tokenizer(filename='./tokenizer.json'):
    #This function loads a tokenizer
    with open(filename) as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)
        
    return tokenizer

def lemma_all_tweets(nlp, tweets, perc_message=5):
	new_tweets = list()
	print('Starting...')
	
	tic = datetime.now() 
	toc = lambda: (datetime.now() - tic).total_seconds()	
	
	i = 0
	N = len(tweets)
	i_msg = int(perc_message*N/100)
	
	for tweet in tweets:
		new_tweets.append(lemmatize_tweet(nlp(tweet)))
		i += 1
		if(i%i_msg==0):
			print('{}% completed'.format(int(perc_message*i/i_msg)))
	
	print('Execution time: {} min'.format(toc()/60))
	return new_tweets
