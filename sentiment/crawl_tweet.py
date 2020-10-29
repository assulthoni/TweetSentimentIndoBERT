import tweepy
import json
from tweepy import OAuthHandler
import re
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup
from django.conf import settings

consumer_key = settings.CONSUMER_KEY
consumer_secret = settings.CONSUMER_SECRET
access_token = settings.ACCESS_TOKEN
access_secret = settings.ACCESS_SECRET
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
# load the twitter API via tweepy
api = tweepy.API(auth)

tok = WordPunctTokenizer()

pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
pat3 = r'RT '
combined_pat = r'|'.join((pat1, pat2, pat3))

def tweet_cleaner(text):
  soup = BeautifulSoup(text, 'lxml')
  souped = soup.get_text()
  stripped = re.sub(combined_pat, '', souped)
  try:
      clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
  except:
      clean = stripped
  letters_only = re.sub("[^a-zA-Z]", " ", clean)
  lower_case = letters_only.lower()
  # During the letters_only process two lines above, it has created unnecessay white spaces,
  # I will tokenize and join together to remove unneccessary white spaces
  words = tok.tokenize(lower_case)
  result = (" ".join(words)).strip()
  return (result[:254]) if len(result) > 254 else result

def get_data(keyword, maxTweets=50):
  print("> Fetching Twitter")
  searchQuery = keyword + " -filter:retweets"
  public_tweets = []
  sinceId = None

  tweetsPerQry = 100
  max_id = -1
  result = []
  tweetCount = 0
  while tweetCount < maxTweets:
    try:
      if (max_id <= 0):
        if (not sinceId):
            new_tweets = api.search(q=searchQuery, tweet_mode="extended", count=tweetsPerQry)
        else:
            new_tweets = api.search(q=searchQuery, tweet_mode="extended", count=tweetsPerQry,
                                    since_id=sinceId)
      else:
        if (not sinceId):
            new_tweets = api.search(q=searchQuery, tweet_mode="extended", count=tweetsPerQry,
                                    max_id=str(max_id - 1))
        else:
            new_tweets = api.search(q=searchQuery, tweet_mode="extended", count=tweetsPerQry,
                                    max_id=str(max_id - 1),
                                    since_id=sinceId)
      if not new_tweets:
        print("No more tweets found")
        break
      
      print("> Tweet fetched")
      print("  Got " + str(len(new_tweets)) + " From API")
      cleaned_tweets = []
      for t in new_tweets:
        cleaned = tweet_cleaner(t.full_text)
        if (len(cleaned) > 10):
          cleaned_tweets.append(cleaned)
      result += cleaned_tweets
      print("  Got " + str(len(cleaned_tweets)) + " Cleaned Tweet")

      tweetCount = len(result)
      print("  Current tweet count: " + str(tweetCount))
      
      max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        break
        
  return result[:maxTweets]
