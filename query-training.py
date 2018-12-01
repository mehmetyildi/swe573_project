# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tweepy
from datetime import date, timedelta
import datetime
import time


consumer_key= "awoaZc3Z0rube5PWTTII1ZmZG"
consumer_secret= "Qh1DZFO4txoK7eTxPr0zJFAU4DQkcBtCl0yHa2unu6cbwCQdWf"
access_token="2895970625-xf4G18XIjZ3CbC471qfirH1zpRgVVcXx4GhspR0"
access_token_secret="uRgmoD818TbpK66FipL0g7SQP4rfarC8OObkWIbhcFma2"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)
auth.secure=True
authUrl = auth.get_authorization_url()
#go to this url
print ("Please Visit This link and authorize the app ==> " + authUrl)
print ("Enter The Authorization PIN")

#writing access tokes to file
pin = input().strip()
token = auth.get_access_token(verifier=pin)
auth.set_access_token(token[0], token[1])
api = tweepy.API(auth)
tweet = api.get_status(id=1052234937951277056)
api.update_status('@'+tweet.screen_name+' '+"Merhaba", tweet.tweet_id)
accessTokenFile = open("accessTokens","w")
accessTokenFile.write(token[0]+'\n')
accessTokenFile.write(token[1]+'\n')

#u=api.get_user("@kadikoybelediye")
#def resident(user,town):
#    return api.show_friendship(source_screen_name=user,target_screen_name=town)[0].following
#
#
#
#query="gitar OR davul OR flüt OR piyano OR mızrap OR klarnet OR çalgı OR keman -filter:retweets"
#
#yesterday = date.today() - timedelta(1)
#today = date.today()
#
#max_tweets=1000
#i=0
#currentTime = str(datetime.datetime.now().date())
#filtered_tweets=[]
#
#new_tweets = api.user_timeline(screen_name = "@mehmetyildi16",count=200, tweet_mode="extended")
#for tweets in new_tweets:
#    filtered_tweets.append(tweets)
#for tweet in filtered_tweets:
#    print(tweet.id)
#
#tweet = api.get_status(id=1052234937951277056)
#print(tweet.text)
#searched_tweets = [status for status in tweepy.Cursor(api.search, tweet_mode="extended", q=query,result_type="recent",include_entities=True,since = yesterday,lang='tr').items(max_tweets)]
#for tweets in searched_tweets:
#    filtered_tweets.append(tweets)
#print(len(filtered_tweets))
#time.sleep(60)    
#try:    
#    for tweet in filtered_tweets:
#        username=tweet.user.screen_name
#        i=i+1
#        if i%60 ==0:
#            time.sleep(60*15)
#        town1="@kadikoybelediye"
#        town2="@MaltepeBelTr"
#        town3="@uskudarbld"
#        
#        if(resident(username,town1)):
#            print(username)
#            print(town1)
#            print(tweet.full_text)
#            print(tweet.created_at)
#            continue
#        if (resident(username,town2)):
#            print(username)
#            print(town2)
#            print(tweet.full_text)
#            print(tweet.created_at)
#            continue
#        if (resident(username,town3)):
#            print(username)
#            print(town3)
#            print(tweet.full_text)
#            print(tweet.created_at)
#            continue 
#except tweepy.error.TweepError:
#    print (i)
#    print("Reached Twitter rate limit")
    


#ids = []
#for page in tweepy.Cursor(api.followers_ids, screen_name="@kadikoybelediye").pages():
 #   ids.extend(page)
 #   time.sleep(60)
 #   print(page)

#print (len(ids))

#query = 'python'
#max_tweets = 10000
#searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
#tweets = []
#for tweet in searched_tweets:
#    if tweet.created_at.date() < today and tweet.created_at.date() > yesterday:
#        tweets.append(tweet)
#for tweet in tweets:
#    print(tweet.text)
 