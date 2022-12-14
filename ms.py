# -*- coding: utf-8 -*-
"""MS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L9Nt1ThRkSqWiwlSJJSUGJf2aeJQViP-
"""

import tweepy
from textblob import TextBlob as tb
from wordcloud import WordCloud as wc
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from google.colab import files
uploaded = files.upload()

log = pd.read_csv('login.csv')

consumer_key = log['key'][0]
consumer_secret = log['key'][1]
Access_token = log['key'][2]
token_secret = log['key'][3]

authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)
authenticate.set_access_token(Access_token, token_secret)
api = tweepy.API(authenticate, wait_on_rate_limit = True)

posts = api.user_timeline(screen_name = 'Amazon', count= 500, lang = 'en', tweet_mode ='extended')
print("show the 5 tweets: \n")
i =1
for tweet in posts[0:5]:
  print(str(i) + ') '+ tweet.full_text + '\n')
  i = i + 1

df = pd.DataFrame([ tweet.full_text for tweet in posts], columns = ['Tweets'])
df.head

def cleanTxt(text):
  text = re.sub(r'@[A-Za-z0-9]+', '', text)
  text = re.sub(r'#', '', text)
  text = re.sub(r'RT[\s]+', '', text)
  text = re.sub(r'https?:\/\/\S+', '', text)
  text = re.sub(r':|_|@', '', text)
  
 
  return text
df['Tweets'] = df['Tweets'].apply(cleanTxt)

df

def getSubjectivity(text):
  return tb(text).sentiment.subjectivity

def getPolarity(text):
  return tb(text).sentiment.polarity

df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)

df

#wordcloud
allWords = ''.join(tweets for tweets in df['Tweets'])
wordCloud = wc(width = 800, height = 500, random_state =12, max_font_size = 119).generate(allWords)

plt.imshow(wordCloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()

#creating function to compute negative, neutral and positive analysis
def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'

df['Analysis'] = df['Polarity'].apply(getAnalysis) 

df

#print all +ve tweets
k=1
sortedDF = df.sort_values(by = ['Polarity'])
for i in range(0, sortedDF.shape[0]):
  if sortedDF['Analysis'][i] == 'Positive':
    print(str(k) + ') ' + sortedDF['Tweets'][i])
    print()
    k = k+1

#print -ve tweets
j=1
sortedDF = df.sort_values(by = ['Polarity'], ascending ='False')
for i in range(0, sortedDF.shape[0]):
  if sortedDF['Analysis'][i] == 'Negative':
    print(str(j) + ') ' + sortedDF['Tweets'][i])
    print()
    j = j+1

#print neutral tweets
j=1
sortedDF = df.sort_values(by = ['Polarity'])
for i in range(0, sortedDF.shape[0]):
  if sortedDF['Analysis'][i] == 'Neutral':
    print(str(j) + ') ' + sortedDF['Tweets'][i])
    print()
    j = j+1

def getAnalysis(score):
  if score < 0:
    return -1.0
  elif score == 0:
    return 0.0
  else:
    return 1.0

df['Analysis'] = df['Polarity'].apply(getAnalysis) 

df

#plot the polarity and subjectivity

plt.figure(figsize=(8,4))
for i in range(0, df.shape[0]):
  plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color ='Blue')

plt.title('Sentimental Analysis')
plt.xlabel('polarity')
plt.ylabel('Subjectivity')
plt.show()

#get percentage of +ve tweets
ptweets = df[df.Analysis ==1.0]
ptweets = ptweets['Tweets']

round(( ptweets.shape[0] / df.shape[0])*100 ,1)

#get percent of -ve tweets
ntweets = df[df.Analysis == -1.0]
ntweets = ntweets['Tweets']

round(( ntweets.shape[0] / df.shape[0])*100 ,1)

#get percent 
Ntweets = df[df.Analysis == 0.0]
Ntweets = Ntweets['Tweets']

round(( Ntweets.shape[0] / df.shape[0])*100,1)

#show value
df['Analysis'].value_counts()
#plot
plt.title('Sentimental Analysis of Amazon')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind = 'bar')
plt.show()

!pip install treeinterpreter

from sklearn.model_selection import train_test_split
from treeinterpreter import treeinterpreter as ti
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn import svm
from sklearn.svm import SVR 

from sklearn.metrics import mean_squared_error
from math import sqrt

X = df.drop(["Tweets"],axis = 1)
#X = df.drop("Tweets", axis=1)
y = df["Analysis"]

4!pip install sklearn

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state= 1)
from sklearn.linear_model import LinearRegression as lr

#fit the train and test 
 log = lr()
 log.fit(X_train, y_train)

pred = log.predict(X_test)

from sklearn.metrics import accuracy_score

log.score(X_test, y_pred)*100

"""len(X_train),len(X_test)"""

len(y_train),len(y_test)

X_train

X_test