from django.conf.urls import url
from tweets import views

app_name='tweets'

urlpatterns= [
    url(r'^$',views.tweet_list,name='tweet_list'),

]
