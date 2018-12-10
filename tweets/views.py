from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Tweet,Reply,Reported
from . twitter import  show_tweets,reply_tweet,tweet_kill
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from social_django.models import AbstractUserSocialAuth, UserSocialAuth
from django.contrib import messages


# Create your views here.


@login_required
def tweet_list(request):
    tweet_list = Tweet.objects.order_by('tweet_date')[:100]
    # page = request.GET.get('page', 1)
    # paginator = Paginator(tweets, 10)
    # try:
    #     tweets = paginator.page(page)
    # except PageNotAnInteger:
    #     tweets = paginator.page(1)
    # except EmptyPage:
    #     tweets = paginator.page(paginator.num_pages)
    if request.method=='POST':
        area=Tweet.objects.filter(tweet_id=request.POST['tweet_id']).get().area
        keyword=Tweet.objects.filter(tweet_id=request.POST['tweet_id']).get().keyword
        reply_tweet(request,request.user.pk,request.POST['tweet_id'],request.POST['tweet_text'],request.POST['screen_name'],area,keyword)
    page = request.GET.get('page', 1)
    paginator = Paginator(tweet_list, 10)
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)
    return render(request, 'tweets/tweet_list.html', {'tweets': tweets})

@login_required
def delete_tweet(request):
    id=request.POST['tweet_id']
    tweet_kill(request,request.user.pk,id)
    return redirect('tweets:tweet_list')

@login_required
def report_tweet(request,id):
    if request.method=='POST' and request.POST['report_reason']:
        report=Reported(tweet=Tweet.objects.filter(pk=id).get(),report_reason=request.POST['report_reason'])
        report.save()
        messages.info(request,'Your report is successfully saved. Thank you for your input.')
        return redirect('tweets:tweet_list')
    return render(request,'tweets/report_modal.html',{'id':id})

@login_required
def tweet_fetch(request):
    keywords=[]
    areas=[]
    for keyword in request.user.selected_keywords.all():
        keywords.append(keyword.name)
    for area in request.user.selected_areas.all():
        areas.append(area.twittername)
    show_tweets(keywords,areas)
    print('finished out')
    return redirect('tweets:tweet_list')
    print('finished out2')
