from django.conf.urls import url
from tweets import views

app_name='tweets'

urlpatterns= [
    url(r'^$',views.tweet_fetch,name='tweet_fetch'),
    url(r'list/$',views.tweet_list,name='tweet_list'),
    url(r'delete/$',views.delete_tweet,name='delete_tweet'),
    url(r'report/(?P<id>\d+)',views.report_tweet,name='report_tweet'),
]
