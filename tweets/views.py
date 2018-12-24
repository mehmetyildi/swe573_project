from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Tweet,Reply,Reported
from . twitter import  show_tweets,reply_tweet,tweet_kill
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from social_django.models import AbstractUserSocialAuth, UserSocialAuth
from django.contrib import messages
from datetime import date, timedelta
from filter.models import UserMarketSettings


# Create your views here.


@login_required
def tweet_list(request):#Returns view that lists the tweets that matches areas and keywords and tweeted since yesterday.
    yesterday = date.today() - timedelta(1)
    tweet_list = Tweet.objects.filter(user=request.user) and Tweet.objects.filter(tweet_date__gte= yesterday).order_by('tweet_date')
    settings=UserMarketSettings.objects.filter(user=request.user).first()#To show user settings, areas and keywords on the view.
    if request.method=='POST':#if user wants to reply a tweet.
        area=Tweet.objects.filter(tweet_id=request.POST['tweet_id']).get().area# to keep area hit.
        keyword=Tweet.objects.filter(tweet_id=request.POST['tweet_id']).get().keyword# to keep keyword hit.
        reply_tweet(request,request.user.pk,request.POST['tweet_id'],request.POST['tweet_text'],request.POST['screen_name'],area,keyword)
    page = request.GET.get('page', 1)#Paginate and show only 10 tweets per page
    paginator = Paginator(tweet_list, 10)
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)
    return render(request, 'tweets/tweet_list.html', {'tweets': tweets,'settings':settings})

@login_required
def delete_tweet(request):#deletes a replied tweet.
    id=request.POST['tweet_id']
    tweet_kill(request,request.user.pk,id)
    return redirect('tweets:tweet_list')

@login_required
def report_tweet(request,id):#report a tweet as not useful.
    if request.method=='POST' and request.POST['report_reason']:
        report=Reported(tweet=Tweet.objects.filter(pk=id).get(),report_reason=request.POST['report_reason'])
        report.save()
        messages.info(request,'Your report is successfully saved. Thank you for your input.')
        return redirect('tweets:tweet_list')
    return render(request,'tweets/report_modal.html',{'id':id})

@login_required
def tweet_fetch(request):#fetch tweets before showing tweet_list page.
    keywords=[]
    areas=[]
    for keyword in request.user.selected_keywords.all():
        keywords.append(keyword.name)
    for area in request.user.selected_areas.all():
        areas.append(area.twittername)
    show_tweets(keywords,areas,request.user)
    return redirect('tweets:tweet_list')
