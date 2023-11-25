#!/usr/bin/env python
# coding: utf-8

# In[7]:
import tweepy
import textblob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
# In[8]:
# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
bearer_token = ""

client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)


# In[9]:
def analyze_sentiment(username):
    # Get the 200 most recent tweets from the user
    user=client.get_user(username=username).data
    user_id = user.id
    tweets = client.get_users_tweets(id=user_id, max_results = 100,tweet_fields=['text'])
   # Analyze the sentiment of each tweet
    tweet_sentiments = []
    for tweet in tweets.data:
       text = tweet.text
       analysis = textblob.TextBlob(text)
       tweet_sentiments.append(analysis.sentiment)

    return tweet_sentiments
# In[10]:
def create_wordcloud(username):
    # Get the 100 most recent tweets from the user
    user=client.get_user(username=username).data
    user_id = user.id
    tweets = client.get_users_tweets(id=user_id, max_results = 100,tweet_fields=['text'])
    # Create a word cloud from the tweets
    text = " ".join([tweet.text for tweet in tweets.data])
    wordcloud = WordCloud(width=800, height=800, random_state=21, max_font_size=110).generate(text)

    return wordcloud
# In[11]:
def display_analysis(username):
    tweet_sentiments = analyze_sentiment(username)
    wordcloud = create_wordcloud(username)
    # Plot the sentiment analysis
    fig = plt.figure(figsize=(10,10), facecolor='w')
    plt.hist([s.polarity for s in tweet_sentiments], bins=10)
    plt.xlabel("Sentiment")
    plt.ylabel("Frequency")
    st.pyplot(fig)
    # Plot the word cloud
    fig2 = plt.figure(figsize=(10, 10), facecolor='k')
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig2)
# In[12]:
# Streamlit UI
def main():
    st.title("Twitter Sentiment Analysis")
    username = st.text_input("Enter the username of the Twitter user:")
    if username:
        display_analysis(username)

if __name__ == "__main__":
    main()


# In[ ]:




