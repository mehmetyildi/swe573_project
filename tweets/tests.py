from django.test import TestCase
from . twitter import resident, fetch, show_tweets
import json
from filter.models import Keywords, Locations
from django.contrib.auth.models import User
from .models import Tweet
# Create your tests here.

class TwitterTest(TestCase):
    def test_resident(self):
        result=resident("@mehmetyildi","@kadikoybelediye")
        self.assertEquals(result,1)

    def test_keyword(self):
        keyword="gitar"
        result=fetch(keyword)

        for tweet in result:
            self.assertEquals(keyword.lower() in json.dumps(tweet._json).lower(),True)

    def test_tweet_fetch(self):
        user=User(username='testuser1', password='12345', is_active=True, is_staff=True, is_superuser=True).save()
        Locations(name="Kadiköy",twittername="@kadikoybelediye").save()
        Keywords(name="gitar").save()
        Keywords(name="davul").save()
        Keywords(name="klarnet").save()
        keywords=[]
        areas=[]
        for keyword in Keywords.objects.all():
            keywords.append(keyword.name)
        for area in Locations.objects.all():
            areas.append(area.twittername)
        show_tweets(user=user, areas=areas, keywords=keywords)
        print("Tweet count: "+str(len(Tweet.objects.all())))
        self.assertLess(len(Tweet.objects.all()),15)
        for tweets in Tweet.objects.all():
            self.assertEqual(resident(tweet.user.screen_name,area[0].twittername),1)
