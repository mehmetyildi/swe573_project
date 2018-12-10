from django.db import models

# Create your models here.
class Tweet(models.Model):
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE, null=True, blank=True)
    tweet_id = models.CharField(max_length=250, null=True, blank=True)
    screen_name=models.CharField(max_length=250, null=True, blank=True)
    tweet_text = models.TextField()
    tweet_date = models.DateField(null=True)
    tweet_url = models.CharField(max_length=500, blank=True, null=True)
    keyword=models.CharField(max_length=250, null=True, blank=True)
    area=models.CharField(max_length=250, null=True, blank=True)
    stamp=models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.tweet_text

    def hasReply(self):
        if(self.threaded_reply.count()>0):
            return True
        else:
            return False

    def hasReport(self):
        if(self.reported_tweet.count()>0):
            return True
        else:
            return False

class Reply(models.Model):
    tweet=models.ForeignKey(Tweet,on_delete=models.CASCADE, null=True, blank=True,related_name='threaded_reply')
    reply_id=models.CharField(max_length=250, null=True, blank=True)

class Reported(models.Model):
    tweet=models.ForeignKey(Tweet,on_delete=models.CASCADE, null=True, blank=True,related_name='reported_tweet')
    report_reason=models.CharField(max_length=250, null=True, blank=True)
