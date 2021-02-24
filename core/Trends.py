import datetime
import requests
from bs4 import BeautifulSoup
from data import constants
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import random, re, string
from nltk.twitter import Twitter


class TrendResearch():

    def __init__(self):
        print("Searching for latest trends")
    # Check yahoo for latest gainers
    def researchBot(self):
        print(datetime.date.today())
        url = "https://finance.yahoo.com/gainers"
        crawl = requests.session()
        response = crawl.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        for i in soup.find_all('a', class_="Fw(600)"):
            daily = open("daily.txt", "a")
            daily.write(i.get_text() + "\n")
            daily.close()

    def analyze_data(self, data, user, name):
        print("[*] Analyzing...")
        print("User: " + user)
        print("Name: " + name)
        print("Tweet =>")
        print(data)
        print("\n")
        self.nlp_(data)

    def remove_noise(tweet_tokens, stop_words=()):

        cleaned_tokens = []

        for token, tag in pos_tag(tweet_tokens):
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                           '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
            token = re.sub("(@[A-Za-z0-9_]+)", "", token)

            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'

            lemmatizer = WordNetLemmatizer()
            token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        return cleaned_tokens

    def get_all_words(cleaned_tokens_list):
        for tokens in cleaned_tokens_list:
            for token in tokens:
                yield token

    def get_tweets_for_model(cleaned_tokens_list):
        for tweet_tokens in cleaned_tokens_list:
            yield dict([token, True] for token in tweet_tokens)

    def tweeter(self):
        tw = Twitter()
        tw.tweets(keywords='love, hate', limit=10)

    def nlp_(self, tweet):
        stop_words = stopwords.words('english')
        positive_cleaned_tokens_list = []
        negative_cleaned_tokens_list = []

        # for tokens in positive_tweet_tokens:
        #     positive_cleaned_tokens_list.append(self.remove_noise(tokens, stop_words))
        #
        # for tokens in negative_tweet_tokens:
        #     negative_cleaned_tokens_list.append(self.remove_noise(tokens, stop_words))

        all_pos_words = self.get_all_words(positive_cleaned_tokens_list)

        freq_dist_pos = FreqDist(all_pos_words)
        print(freq_dist_pos.most_common(10))

        positive_tokens_for_model = self.get_tweets_for_model(positive_cleaned_tokens_list)
        negative_tokens_for_model = self.get_tweets_for_model(negative_cleaned_tokens_list)

        positive_dataset = [(tweet_dict, "Positive")
                            for tweet_dict in positive_tokens_for_model]

        negative_dataset = [(tweet_dict, "Negative")
                            for tweet_dict in negative_tokens_for_model]

        dataset = positive_dataset + negative_dataset

        random.shuffle(dataset)

        train_data = dataset[:7000]
        test_data = dataset[7000:]

        classifier = NaiveBayesClassifier.train(train_data)

        print("Accuracy is:", classify.accuracy(classifier, test_data))

        print(classifier.show_most_informative_features(10))

        mock_tweet = "money good. i likez money"

        custom_tokens = self.remove_noise(word_tokenize(mock_tweet))

        print(mock_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))



