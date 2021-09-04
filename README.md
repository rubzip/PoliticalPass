# PoliticalPass

Deep Learning project. The objetive is to predict if a (spanish) twitter account is left-wing or right-wing based on most often tweetted words.

The most important files are:

* `config.py` : Python file that stores API keys.

* `datos.csv` : Info about all users analayzed.

* `data_mining.ipynb` : Download the `number_tweets` last tweets from each user and are stored in `raw_tweets.csv`.  

* `data_cleaning.ipynb` : 

## Requirements

This project uses the following Python libraries

* `spaCy` : Used to tokenize the article into sentences and words.
* `PRAW` : Makes the use of the Reddit API very easy.
* `Requests` : To perform HTTP `get` requests to the articles urls.
* `BeautifulSoup` : Used for extracting the article text.
* `html5lib` : This parser got better compatibility when used with `BeautifulSoup`.
* `tldextract` : Used to extract the domain from an url.
* `wordcloud` : Used to create word clouds with the article text.

After installing the `spaCy` library you must install a language model to be able to tokenize the article.

For `Spanish` you can run this one:

`python -m spacy download es_core_news_sm`

For other languages please check the following link: https://spacy.io/usage/models

## Reddit Bot

The bot is simple in nature, it uses the `PRAW` library which is very straightforward to use. The bot polls a subreddit every 10 minutes to get its latest submissions.

It first detects if the submission hasn't already been processed and then checks if the submission url is in the whitelist. This whitelist is currently curated by myself.

If the post and its url passes both checks then a process of web scraping is applied to the url, this is where things start getting interesting.

Before replying to the original submission it checks the percentage of the reduction achieved, if it's too low or too high it skips it and moves to the next submission.

## Web Scraper

Currently in the whitelist there are already more than 300 different websites of news articles and blogs. Creating specialized web scrapers for each one is simply not feasible.

The second best thing to do is to make the scraper as accurate as possible.

We start the web scraper on the usual way, with the `Requests` and `BeautifulSoup` libraries.

```python
with requests.get(article_url) as response:
    
    if response.encoding == "ISO-8859-1":
        response.encoding = "utf-8"

    html_source = response.text

for item in ["</p>", "</blockquote>", "</div>", "</h2>", "</h3>"]:
    html_source = html_source.replace(item, item+"\n")

soup = BeautifulSoup(html_source, "html5lib")
```






https://towardsdatascience.com/email-spam-detection-1-2-b0e06a5c0472

https://likegeeks.com/es/tutorial-de-nlp-con-python-nltk/#Implementaciones_del_NLP
RNN

## TAREAS
 * Añadir un .gitnore https://medium.com/black-tech-diva/hide-your-api-keys-7635e181a06c
 * Implemetar manera de minar data de manera paralela
 * Limpiar los datos
 * Crear diccionario de palabras
 * Aumentar el dataset (más cuentas y más twits)
 * Subir como otro proyeco a github la version buena sin las APIs
 * wordcloud
 * ordenar por carpetas
 * añadir mas graficas, balanceo de datos

## Requeriments
 * python3
 * tweetpy
 * NLKT
