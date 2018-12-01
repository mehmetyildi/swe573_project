from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Tweet
from . twitter import save_to_db, set_active, set_inactive, user_tweets, show_tweets,reply_tweet
from django.core.paginator import Paginator
from django.http import HttpResponse
from social_django.models import AbstractUserSocialAuth, UserSocialAuth

# Create your views here.



def tweet_list(request):
    tweets = Tweet.objects.order_by('tweet_date')[:100]
    # page = request.GET.get('page', 1)
    # paginator = Paginator(tweets, 10)
    # try:
    #     tweets = paginator.page(page)
    # except PageNotAnInteger:
    #     tweets = paginator.page(1)
    # except EmptyPage:
    #     tweets = paginator.page(paginator.num_pages)
    if request.method=='POST':
        reply_tweet(request.user.pk,request.POST['tweet_id'],request.POST['tweet_text'],request.POST['screen_name'])

    return render(request, 'tweets/tweet_list.html', {'tweets': tweets})


def tweet_set_inactive(request, pk):
    set_inactive(pk)
    return redirect('tweets:tweet_list')


def tweet_set_active(request, pk):
    set_active(pk)
    return redirect('tweets:tweet_list')


def tweet_fetch(request):
    keywords=[]
    areas=[]
    for keyword in request.user.selected_keywords.all():
        keywords.append(keyword.name)
    for area in request.user.selected_areas.all():
        areas.append(area.twittername)
    show_tweets(keywords,areas)
    return redirect('tweets:tweet_list')
