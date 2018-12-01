from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from filter.models import Locations, Markets, UserMarketSettings,Keywords,UserAreas,KeywordOwner
from django.views.generic import (TemplateView,ListView,
                                DetailView,CreateView,
                                UpdateView,DeleteView)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
# Create your views here.
# class UserMarketSettingsCreate(TemplateView):
#     template_name='filter/create.html'
#     def get_context_data(self, **kwargs):
#         context = super(UserMarketSettingsCreate, self).get_context_data(**kwargs)
#         context['locations']=Locations.objects.order_by('id')
#         context['markets']=Markets.objects.order_by('id')
#         return context
@login_required
def create(request):
    all_markets=Markets.objects.order_by('id')
    all_locations=Locations.objects.order_by('id')

    if request.method=='POST':
        market=Markets.objects.get(pk=request.POST['market'])
        location=Locations.objects.get(pk=request.POST['location'])
        setting=UserMarketSettings()
        setting.user=request.user
        setting.market=market
        setting.location=location
        setting.save()
        return redirect('filter:filters')

    return render(request, 'filter/create.html',context={'locations':all_locations,'markets':all_markets})
@login_required
def update(request,pk):
    user=User.objects.get(pk=pk)
    all_markets=Markets.objects.order_by('id')
    all_locations=Locations.objects.order_by('id')
    set=UserMarketSettings.objects.filter(user=user).first()
    selected_location=set.location
    selected_market=set.market
    if request.method=='POST':
        market=Markets.objects.get(pk=request.POST['market'])
        location=Locations.objects.get(pk=request.POST['location'])
        set.user=request.user
        set.market=market
        set.location=location
        set.save()
        return redirect('filter:update_filters',pk=(pk))

    return render(request, 'filter/update.html',context={'locations':all_locations,'markets':all_markets,'selected_location':selected_location,'selected_market':selected_market})

@login_required
def filters(request):
    setting=UserMarketSettings.objects.filter(user=request.user.id).first()
    userareas=UserAreas.objects.all()
    locations=Locations.objects.order_by('id')
    keywords=Keywords.objects.order_by('id')
    market_info={'locations':locations,'keywords':keywords}
    user=request.user
    if request.method=='POST':

        for loc in request.POST.getlist('location'):
            location=Locations.objects.get(pk=loc)
            UserAreas.objects.create(user=request.user,area=location)
        for key in request.POST.getlist('keywords'):
            obj,created=Keywords.objects.get_or_create(name=key)
            KeywordOwner.objects.create(owner=request.user,keyword=obj)


        return redirect('tweets:tweet_list')
    return render(request, 'filter/filters.html',context=market_info)
@login_required
def update_filters(request,pk):
    setting=UserMarketSettings.objects.filter(user=request.user.id).first()
    user=User.objects.get(pk=pk)
    userareas=user.selected_areas.all()
    userkeywords=user.selected_keywords.all()
    locations=Locations.objects.order_by('id')
    keywords=Keywords.objects.order_by('id')
    market_info={'locations':locations,'keywords':keywords,'selected_areas':userareas,'selected_keywords':userkeywords}
    user=request.user
    if request.method=='POST':
        user.selected_areas.clear()
        user.selected_keywords.clear()
        for loc in request.POST.getlist('location'):
            location=Locations.objects.get(pk=loc)
            UserAreas.objects.create(user=request.user,area=location)
        for key in request.POST.getlist('keywords'):
            obj,created=Keywords.objects.get_or_create(name=key)
            KeywordOwner.objects.create(owner=request.user,keyword=obj)
        return redirect('tweets:tweet_list')
    return render(request, 'filter/filters_update.html',context=market_info)

@login_required
def tweets(request):
    user=request.user
    areas=user.selected_areas.all()
    keywords=user.selected_keywords.all()
    return render(request, 'filter/tweets.html',context={'user':user, 'areas':areas, 'keywords':keywords})


@login_required
def home(request):
    if request.user.selected_areas.count()>0:
        return redirect('tweets:tweet_list')
    else:
        return redirect('filter:create')
    user=request.user
    areas=user.selected_areas.all()
    keywords=user.selected_keywords.all()
    return JsonResponse({'areas':areas,'keywords':keywords})
    return render(request, 'filter/home.html')
