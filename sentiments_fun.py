import tweepy
from textblob import TextBlob

import numpy as np
import operator

consumer_key = '9g4nXuw7FEMGuoZVg0QtwMgTg'
consumer_secret = 'TjezDJ7xoDXvqJFZDtDlNJYTmMmfHAVUevF1bafyFRJiafehta'

access_token = '973830516691611648-nYuLxBk0T1m0Ki8t2PN6GjSRQBtqCTy'
access_token_secret = 'YGsgrmQkFawCmzTNiTUyJNk8UMvyWw1W6rC3naWmukXGy'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Step 2 - Prepare query features

# List of accounts linked to ALC4
account_names = ['Pluralsight', 'Google in Africa', '150DaysOfALC4']
#Hashtag related to ALC4
name_of_topic = "150DaysOfALC4"
#Dates of interest
since_date = "2019-06-29"
until_date = "2019-07-03"

#Step 2b - Function of labelisation of analysis
def get_label(analysis, threshold = 0):
	if analysis.sentiment[0]>threshold:
		return 'Positive'
	else:
		return 'Negative'


#Step 3 - Retrieve Tweets and Save Them
all_polarities = dict()
for account in account_names:
	this_account_polarities = []
	#Get the tweets about the topic and the accounts between the dates
	this_account_tweets = api.search(q=[name_of_topic, account], count=100, since=since_date, until=until_date)
	#Save the tweets in csv
	with open('%s_tweets.csv' % account, 'wb') as this_account_file:
		this_account_file.write('tweet, sentiment_label\n'.encode('utf-8'))
		for tweet in this_account_tweets:
			analysis = TextBlob(tweet.text)
			#Get the label corresponding to the sentiment analysis
			this_account_polarities.append(analysis.sentiment[0])
			this_account_file.write(('%s, %s\n' % (tweet.text.encode('utf-8'), get_label(analysis))).encode('utf-8'))

	#Save the mean for final results
all_polarities[account] = np.mean(this_account_polarities)		


#Step bonus - Print a Result
sorted_analysis = sorted(all_polarities.items(), key=operator.itemgetter(1), reverse=True)
print('Mean Sentiment Polarity in descending order :')
for account, polarity in sorted_analysis:
	print('%s : %0.3f' % (account, polarity))

