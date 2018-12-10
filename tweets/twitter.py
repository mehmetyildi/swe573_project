import tweepy
from tweepy.auth import OAuthHandler
#
from .models import Tweet,Reply
from pprint import pprint
from social_django.models import AbstractUserSocialAuth, UserSocialAuth
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.contrib import auth
import datetime
import time
import json
from filter.models import Locations,Keywords,AreaHit,KeywordHit
from django.contrib import messages

json_data = open('config.json')
data = json.loads(json_data.read())
consumer_key= data.get('consumer_key', "")
consumer_secret= data.get('consumer_secret', "")



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
yesterday = date.today() - timedelta(1)
today = date.today()
max_tweets=10
i=1
currentTime = str(datetime.datetime.now().date())
tweets=[]
keywords=[]
filtered_tweets=[]
try_number=0
final_tweets=[]

def resident(user,town):
    return api.show_friendship(source_screen_name=user,target_screen_name=town)[0].following

def fetch(keyword):
    filtered_tweets[:]=[]
    print("querying "+keyword+" keyword")
    query=keyword+" -filter:retweets"
    searched_tweets = [status for status in tweepy.Cursor(api.search, tweet_mode="extended", q=query,result_type="recent",include_entities=True,since = yesterday,lang='tr').items(3)]
    for tweets in searched_tweets:
        filtered_tweets.append(tweets)
    #         print(len(filtered_tweets))
    #     for original_tweet in filtered_tweets:
    #         new_tweet = Tweet(tweet_id = original_tweet.id, tweet_text=original_tweet.full_text, tweet_date=original_tweet.created_at.date(), screen_name="@"+original_tweet.user.screen_name, is_active = True)
    #         new_tweet.keyword=keyword
    #         new_tweet.stamp=stamp
    #         new_tweet.save()
    #         print(len(Tweet.objects.all()))
    #     filtered_tweets[:]=[]
    # print("db filled")
    print(len(filtered_tweets))
    return filtered_tweets

def filter(area,tweets):
    # tweets=Tweet.objects.filter(stamp=stamp)
    final_tweets[:]=[]
    d=datetime.datetime.now()
    stamp=d.strftime("%d%m%Y%H%M%S")
    tweet_index=0
    for tweet in tweets:
        tweet_index=tweet_index+1
        print("Qurying for tweet number "+str(tweet_index))
        username=tweet.user.screen_name

            # print(".querying "+area+" areas for user "+username)
        if(resident(username,area)):
                # tweet.area=area
                # tweet.save()
            final_tweets.append(tweet)
    return final_tweets

def show_tweets(keywords,areas):
    d=datetime.datetime.now()
    stamp=d.strftime("%d%m%Y%H%M%S")
    try_number=1
    for keyword in keywords:
        tweets=fetch(keyword)
        for area in areas:
            print('here')
            final=filter(area,tweets)
            for tweet in final:
                new_tweet = Tweet(tweet_id = tweet.id, tweet_text=tweet.full_text, tweet_date=tweet.created_at.date(), screen_name="@"+tweet.user.screen_name, is_active = True)
                new_tweet.area=area
                new_tweet.stamp=stamp
                new_tweet.area=keyword
                new_tweet.save()
    print('finished in')
    # d=datetime.datetime.now()
    # stamp=d.strftime("%d%m%Y%H%M%S")
    # for keyword in keywords:
    #     print("querying "+keyword+" keyword")
    #     query=keyword+" -filter:retweets"
    #     searched_tweets = [status for status in tweepy.Cursor(api.search, tweet_mode="extended", q=query,result_type="recent",include_entities=True,since = yesterday,lang='tr').items(max_tweets)]
    #     for tweets in searched_tweets:
    #         filtered_tweets.append(tweets)
    #         print(len(filtered_tweets))
    #     for original_tweet in filtered_tweets:
    #         new_tweet = Tweet(tweet_id = original_tweet.id, tweet_text=original_tweet.full_text, tweet_date=original_tweet.created_at.date(), screen_name="@"+original_tweet.user.screen_name, is_active = True)
    #         new_tweet.keyword=keyword
    #         new_tweet.stamp=stamp
    #         new_tweet.save()
    #         print(len(Tweet.objects.all()))
    #     filtered_tweets[:]=[]
    # print("db filled")
    # tweets=Tweet.objects.filter(stamp=stamp)
    # try_number=0
    # tweet_index=0
    # for tweet in tweets:
    #     tweet_index=tweet_index+1
    #     print("Qurying for tweet number "+str(tweet_index))
    #     username=tweet.screen_name
    #     for area in areas:
    #         if try_number%15==0:
    #             print("waiting 15 minutes on area: "+area)
    #             time.sleep(60*15)
    #         try_number=try_number+1
    #         print(try_number)
    #         print(".querying "+area+" areas for user "+username)
    #         if(resident(username,area)):
    #             tweet.area=area
    #             tweet.save()

def tweet_kill(request,user,id):
    instance = UserSocialAuth.objects.filter(user=user).get()
    oauth_access_token=(instance.access_token).get('oauth_token')
    oauth_access_secret=(instance.access_token).get('oauth_token_secret')
    auth.set_access_token(oauth_access_token, oauth_access_secret)
    api = tweepy.API(auth)
    api.destroy_status(id)
    Reply.objects.filter(reply_id=id).delete()
    messages.info(request,'Your reply is successfully deleted')

def reply_tweet(request,user,tweet_id,tweet_text,screen_name,area,keyword):
    location=User.objects.filter(pk=user).get().settings.first()
    hitarea=Locations.objects.filter(twittername=area).get()
    keyword=Keywords.objects.filter(name=keyword).get()
    AreaHit.gethit(hitarea,location)
    KeywordHit.gethit(keyword,location)
    instance = UserSocialAuth.objects.filter(user=user).get()
    oauth_access_token=(instance.access_token).get('oauth_token')
    oauth_access_secret=(instance.access_token).get('oauth_token_secret')
    auth.set_access_token(oauth_access_token, oauth_access_secret)
    api = tweepy.API(auth)
    try:
        id=api.update_status('@'+screen_name+' '+tweet_text, tweet_id)
        reply=Reply(tweet_id=Tweet.objects.filter(tweet_id=tweet_id).get().pk,reply_id=id.id)
        reply.save()
        messages.info(request,'Your reply is successfully tweeted')
    except:
        messages.warning(request,'Something is wrong about your twitter credentials. Try Logging on again')
