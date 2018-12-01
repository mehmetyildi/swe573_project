from django.db import models

# Create your models here.
class Tweet(models.Model):
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
