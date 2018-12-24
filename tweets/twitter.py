import tweepy
from tweepy.auth import OAuthHandler
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

json_data = open('config.json')#the twitter keys lies in config.json file.
data = json.loads(json_data.read())
consumer_key= data.get('consumer_key', "")
consumer_secret= data.get('consumer_secret', "")



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
yesterday = date.today() - timedelta(1)
today = date.today()
max_tweets=100
i=1
currentTime = str(datetime.datetime.now().date())
tweets=[]
keywords=[]
filtered_tweets=[]
try_number=0
final_tweets=[]

def resident(user,town):#returns true if a user follows the districts mayor's office twitter account. We use this to filter tweets that have the desired keywords.
    return api.show_friendship(source_screen_name=user,target_screen_name=town)[0].following

def fetch(keyword):
    filtered_tweets[:]=[]
    print("querying "+keyword+" keyword")
    query=keyword+" -filter:retweets"
    searched_tweets = [status for status in tweepy.Cursor(api.search, tweet_mode="extended", q=query,result_type="recent",include_entities=True,since = yesterday,lang='tr').items(max_tweets)]
    for tweets in searched_tweets:
        filtered_tweets.append(tweets)
    print(len(filtered_tweets))
    return filtered_tweets

def filter(area,tweets):
    final_tweets[:]=[]
    d=datetime.datetime.now()
    stamp=d.strftime("%d%m%Y%H%M%S")
    tweet_index=0
    for tweet in tweets:
        tweet_index=tweet_index+1
        print("Qurying for tweet number "+str(tweet_index))
        username=tweet.user.screen_name
        try:
            if(resident(username,area)):
                final_tweets.append(tweet)
        except tweepy.error.TweepError:
            print("Waiting 15 minutes due to Twitter limitations")
            time.sleep(60*15)
            if(resident(username,area)):
                final_tweets.append(tweet)
    print("filter finished")
    return final_tweets

def show_tweets(keywords,areas,user):#filters the tweets first through keywords and than areas and writes to the database.
    d=datetime.datetime.now()
    stamp=d.strftime("%d%m%Y%H%M%S")
    try_number=1
    for keyword in keywords:#looks for tweets one keyword at a time and keep the keyword with the tweet. We need this to keep hit values.
        tweets=fetch(keyword)
        for area in areas:#than looks for tweets that has the keyword for areas one at a time for similar reason as the keywords.
            final=filter(area,tweets)
            print("Final number tweets of the keyword: "+keyword)
            print(len(final))
            for tweet in final:#write the filtered tweets to database.
                new_tweet = Tweet(tweet_id = tweet.id, tweet_text=tweet.full_text, tweet_date=tweet.created_at.date(), screen_name="@"+tweet.user.screen_name, is_active = True)
                if(new_tweet.isNew()):
                    new_tweet.area=area
                    new_tweet.stamp=stamp
                    new_tweet.keyword=keyword
                    new_tweet.user=user
                    new_tweet.save()
                    print("A tweet posted by "+tweet.user.screen_name+" is successfully written to the database")



def tweet_kill(request,user,id):#Deletes a reply.
    instance = UserSocialAuth.objects.filter(user=user).get()
    oauth_access_token=(instance.access_token).get('oauth_token')
    oauth_access_secret=(instance.access_token).get('oauth_token_secret')
    auth.set_access_token(oauth_access_token, oauth_access_secret)
    api = tweepy.API(auth)
    api.destroy_status(id)
    Reply.objects.filter(reply_id=id).delete()
    messages.info(request,'Your reply is successfully deleted')

def reply_tweet(request,user,tweet_id,tweet_text,screen_name,area,keyword):#replies a tweet.
    location=User.objects.filter(pk=user).get().settings.first()
    hitarea=Locations.objects.filter(twittername=area).get()
    keyword=Keywords.objects.filter(name=keyword).get()
    AreaHit.gethit(hitarea,location)#keep hit values for further recommendations to other new users.
    KeywordHit.gethit(keyword,location)#keep hit values for further recommendations to other new users.
    instance = UserSocialAuth.objects.filter(user=user).get()
    oauth_access_token=(instance.access_token).get('oauth_token')
    oauth_access_secret=(instance.access_token).get('oauth_token_secret')
    auth.set_access_token(oauth_access_token, oauth_access_secret)
    api = tweepy.API(auth)
    try:
        id=api.update_status('@'+screen_name+' '+tweet_text, tweet_id)
        reply=Reply(tweet_id=Tweet.objects.filter(tweet_id=tweet_id).get().pk,reply_id=id.id,user=User.objects.get(pk=user))
        reply.save()
        messages.info(request,'Your reply is successfully tweeted')
    except:
        messages.warning(request,'Something is wrong about your twitter credentials. Try Logging on again')
