from django.conf.urls import url
from filter import views

app_name='filter'

urlpatterns= [
    url(r'^$',views.create,name='create'),
    url(r'edit/(?P<pk>\d+)/$',views.update,name='update'),
    url(r'filters/$',views.filters,name='filters'),
    url(r'filters/edit_filter/(?P<pk>\d+)/$',views.update_filters,name='update_filters'),
    url(r'tweets/$',views.tweets,name='tweets'),
]
