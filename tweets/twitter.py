import tweepy
from tweepy.auth import OAuthHandler
#
# from .models import Tweet
from pprint import pprint
from social_django.models import AbstractUserSocialAuth, UserSocialAuth
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.contrib import auth
import datetime
import time
import json

json_data = open('config.json')
data = json.loads(json_data.read())
consumer_key= data.get('consumer_key', "")
consumer_secret= data.get('consumer_secret', "")



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)

u=api.get_user("@kadikoybelediye")
def resident(user,town):
    return api.show_friendship(source_screen_name=user,target_screen_name=town)[0].following



query="gitar OR davul OR flüt OR piyano OR mızrap OR klarnet OR çalgı OR keman -filter:retweets"

yesterday = date.today() - timedelta(1)
today = date.today()

max_tweets=1000
i=1
currentTime = str(datetime.datetime.now().date())
tweets=[]
keywords=[]
filtered_tweets=[]
def resident(user,town):
    return api.show_friendship(source_screen_name=user,target_screen_name=town)[0].following

def keywordQuery(keywordArray):
    print("keywordQuery")
    filtered_tweets=[]
    for keyword in keywordArray:
        query=keyword+" -filter:retweets"
        searched_tweets = [status for status in tweepy.Cursor(api.search, tweet_mode="extended", q=query,result_type="recent",include_entities=True,since = yesterday,lang='tr').items(max_tweets)]
        for tweet in searched_tweets:
            filtered_tweets.append(tweet)
        for original_tweet in filtered_tweets:
            new_tweet = Tweet(tweet_id = original_tweet.id, tweet_text=original_tweet.full_text, tweet_date=original_tweet.created_at.date(), screen_name=original_tweet.screen_name, is_active = True)
            new_tweet.keyword=keyword
            filtered_tweets.append(new_tweet)
        print(len(filtered_tweets))
    return filtered_tweets

def areaQuery(tweets,areas):
    print("areaQuery")

    filtered_tweets=[]
    for tweet in tweets:
        username=tweet.screen_name
        for area in areas:
            i=i+1
            if i%15==0:
                time.sleep(60*15)
            if(resident(username,area)):
                tweet.area=area
                filtered_tweets.append(tweet)

    return filtered_tweets

def show_tweets(keywords,areas):
    # tweets=keywordQuery(keywords)
    # filtered_tweets=areaQuery(tweets,areas)
    d=datetime.datetime.now()
    stamp=d.strftime("%d%m%Y%H%M%S")
    for keyword in keywords:
        print("querying "+keyword+" keyword")
        query=keyword+" -filter:retweets"
        searched_tweets = [status for status in tweepy.Cursor(api.search, tweet_mode="extended", q=query,result_type="recent",include_entities=True,since = yesterday,lang='tr').items(max_tweets)]
        for tweets in searched_tweets:
            filtered_tweets.append(tweets)
            print(len(filtered_tweets))
        for original_tweet in filtered_tweets:
            new_tweet = Tweet(tweet_id = original_tweet.id, tweet_text=original_tweet.full_text, tweet_date=original_tweet.created_at.date(), screen_name="@"+original_tweet.user.screen_name, is_active = True)
            new_tweet.keyword=keyword
            new_tweet.stamp=stamp
            new_tweet.save()
            print(len(Tweet.objects.all()))
        filtered_tweets[:]=[]
    print("db filled")
    tweets=Tweet.objects.filter(stamp=stamp)
    try_number=0
    tweet_index=0
    for tweet in tweets:
        tweet_index=tweet_index+1
        print("Qurying for tweet number "+str(tweet_index))
        username=tweet.screen_name
        for area in areas:
            if try_number%15==0:
                print("waiting 15 minutes on area: "+area)
                time.sleep(60*15)
            try_number=try_number+1
            print(try_number)
            print(".querying "+area+" areas for user "+username)
            if(resident(username,area)):
                tweet.area=area
                tweet.save()


    for tweet in tweets:
        if tweet.area=="":
            tweet.delete()


def reply_tweet(user,tweet_id,tweet_text,screen_name):
    instance = UserSocialAuth.objects.filter(user=user).get()
    oauth_access_token=(instance.access_token).get('oauth_token')
    oauth_access_secret=(instance.access_token).get('oauth_token_secret')
    auth.set_access_token(oauth_access_token, oauth_access_secret)
    api = tweepy.API(auth)
    api.update_status('@'+screen_name+' '+tweet_text, tweet_id)

def user_tweets():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API()
    user_tweets = api.user_timeline(count=5)
    return user_tweets

def save_to_db():
    original_tweets = user_tweets()
    for original_tweet in original_tweets:
        if not original_tweet.retweeted:
            if not Tweet.objects.filter(tweet_id=original_tweet.id):
                new_tweet = Tweet(tweet_id = original_tweet.id, tweet_text = original_tweet.text, tweet_date = original_tweet.created_at, is_active = True)
                new_tweet.save()

def set_inactive(pk):
    Tweet.objects.filter(tweet_id = pk).update(is_active = False)

def set_active(pk):
    Tweet.objects.filter(tweet_id = pk).update(is_active = True)
