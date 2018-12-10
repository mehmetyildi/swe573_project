from django.db import models
from tweets import models as tweets

# Create your models here.
class UserMarketSettings(models.Model):
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='settings')
    market=models.ForeignKey('filter.Markets',on_delete=models.CASCADE,)
    location=models.ForeignKey('filter.Locations',on_delete=models.CASCADE,)


    def __str__(self):
        return self.user.username

class Markets(models.Model):
    name=models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class Locations(models.Model):
    name=models.CharField(max_length=200,unique=True)
    twittername=models.CharField(max_length=200,unique=True,blank=True, null=True)
    user=models.ManyToManyField('auth.User', through='UserAreas',related_name='selected_areas')
    settings=models.ManyToManyField(UserMarketSettings, through='AreaHit',related_name='hit_areas')

    def __str__(self):
        return self.name

class Keywords(models.Model):
    name=models.CharField(max_length=200,unique=True)
    user=models.ManyToManyField('auth.User', through='KeywordOwner',related_name='selected_keywords')
    settings=models.ManyToManyField(UserMarketSettings, through='KeywordHit',related_name='hit_keywords')
    def __str__(self):
        return self.name

class KeywordOwner(models.Model):
    keyword = models.ForeignKey(Keywords,related_name='authors',on_delete=models.DO_NOTHING)
    owner = models.ForeignKey('auth.User',related_name='chosenkeywords',on_delete=models.DO_NOTHING)
    on_delete=models.DO_NOTHING

    def __str__(self):
        return self.owner.username

    class Meta:
        unique_together = ('keyword', 'owner')

class UserAreas(models.Model):
    area = models.ForeignKey(Locations,related_name='users',on_delete=models.DO_NOTHING)
    user = models.ForeignKey('auth.User',related_name='areas',on_delete=models.DO_NOTHING)
    on_delete=models.DO_NOTHING

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('area', 'user')

class AreaHit(models.Model):
    area = models.ForeignKey(Locations,related_name='hit',on_delete=models.DO_NOTHING)
    setting = models.ForeignKey(UserMarketSettings,related_name='areas',on_delete=models.DO_NOTHING)
    hit=models.IntegerField(blank=True, null=True, default=0)
    on_delete=models.DO_NOTHING

    def __str__(self):
        return self.area.name

    def gethit(area,location):
        obj,created=AreaHit.objects.get_or_create(area=area,setting=location)
        obj.hit=obj.hit+1
        obj.save()

    class Meta:
        unique_together = ('area', 'setting')

class KeywordHit(models.Model):
    keyword = models.ForeignKey(Keywords,related_name='keywordsettings',on_delete=models.DO_NOTHING)
    setting = models.ForeignKey(UserMarketSettings,related_name='keywords',on_delete=models.DO_NOTHING)
    hit=models.IntegerField(blank=True, null=True, default=0)
    on_delete=models.DO_NOTHING

    def __str__(self):
        return self.keyword.name

    def gethit(keyword,market):
        obj,created=KeywordHit.objects.get_or_create(keyword=keyword,setting=market)
        obj.hit=obj.hit+1
        obj.save()

    class Meta:
        unique_together = ('keyword', 'setting')
