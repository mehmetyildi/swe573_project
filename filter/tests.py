from django.test import TestCase,SimpleTestCase
from django.http import HttpRequest
from django.urls import reverse
from . import views
from . models import Markets,Locations,UserMarketSettings,UserAreas,KeywordOwner,KeywordHit,AreaHit,Keywords
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.test import Client
from rest_framework import status
from .recommender import areaRecommendation, keywordRecommendation

def init():
    Locations(name="Kadiköy",twittername="@kadikoybelediye").save()
    Locations(name="Uskudar").save()
    Locations(name="Beşiktaş").save()
    Locations(name="Şişli").save()
    Locations(name="Mecidiyeköy").save()
    Locations(name="Maltepe").save()

    Keywords(name="gitar").save()
    Keywords(name="davul").save()
    Keywords(name="klarnet").save()
    Keywords(name="flut").save()
    Keywords(name="pena").save()
    Keywords(name="bas gitar").save()

    market=Markets(name='Müzik')
    market.save()

    User(username='testuser1', password='12345', is_active=True, is_staff=True, is_superuser=True).save()
    User(username='testuser2', password='12345', is_active=True, is_staff=True, is_superuser=True).save()
    User(username='testuser3', password='12345', is_active=True, is_staff=True, is_superuser=True).save()
    User(username='testuser4', password='12345', is_active=True, is_staff=True, is_superuser=True).save()
    User(username='testuser5', password='12345', is_active=True, is_staff=True, is_superuser=True).save()
    User(username='testuser6', password='12345', is_active=True, is_staff=True, is_superuser=True).save()

    UserMarketSettings(user=User.objects.get(pk=1),market=Markets.objects.get(pk=1),location=Locations.objects.get(pk=1)).save()
    UserMarketSettings(user=User.objects.get(pk=2),market=Markets.objects.get(pk=1),location=Locations.objects.get(pk=1)).save()
    UserMarketSettings(user=User.objects.get(pk=3),market=Markets.objects.get(pk=1),location=Locations.objects.get(pk=1)).save()
    UserMarketSettings(user=User.objects.get(pk=4),market=Markets.objects.get(pk=1),location=Locations.objects.get(pk=1)).save()
    UserMarketSettings(user=User.objects.get(pk=5),market=Markets.objects.get(pk=1),location=Locations.objects.get(pk=1)).save()
    UserMarketSettings(user=User.objects.get(pk=6),market=Markets.objects.get(pk=1),location=Locations.objects.get(pk=1)).save()

    KeywordHit(keyword=Keywords.objects.get(pk=1),setting=UserMarketSettings.objects.get(pk=1),hit="15").save()
    KeywordHit(keyword=Keywords.objects.get(pk=2),setting=UserMarketSettings.objects.get(pk=2),hit="16").save()
    KeywordHit(keyword=Keywords.objects.get(pk=3),setting=UserMarketSettings.objects.get(pk=3),hit="17").save()
    KeywordHit(keyword=Keywords.objects.get(pk=4),setting=UserMarketSettings.objects.get(pk=4),hit="18").save()
    KeywordHit(keyword=Keywords.objects.get(pk=5),setting=UserMarketSettings.objects.get(pk=5),hit="19").save()
    KeywordHit(keyword=Keywords.objects.get(pk=6),setting=UserMarketSettings.objects.get(pk=6),hit="20").save()

    AreaHit(area=Locations.objects.get(pk=1),setting=UserMarketSettings.objects.get(pk=1),hit="20").save()
    AreaHit(area=Locations.objects.get(pk=2),setting=UserMarketSettings.objects.get(pk=2),hit="19").save()
    AreaHit(area=Locations.objects.get(pk=3),setting=UserMarketSettings.objects.get(pk=3),hit="18").save()
    AreaHit(area=Locations.objects.get(pk=4),setting=UserMarketSettings.objects.get(pk=4),hit="17").save()
    AreaHit(area=Locations.objects.get(pk=5),setting=UserMarketSettings.objects.get(pk=5),hit="16").save()
    AreaHit(area=Locations.objects.get(pk=6),setting=UserMarketSettings.objects.get(pk=6),hit="15").save()



class RecommenderTests(TestCase):
    def test_keyword_recommender(self):
        init()
        keywords=keywordRecommendation(UserMarketSettings.objects.get(pk=1))
        self.assertEqual(len(keywords),5)
        self.assertEqual(keywords[0],Keywords.objects.get(pk=6))
        self.assertEqual(keywords[4],Keywords.objects.get(pk=2))
        self.assertNotIn(Keywords.objects.get(pk=1),iter(keywords))

    def test_area_recommender(self):
        init()
        areas=areaRecommendation(UserMarketSettings.objects.get(pk=1))
        self.assertEqual(len(areas),5)
        self.assertEqual(areas[0],Locations.objects.get(pk=1))
        self.assertEqual(areas[4],Locations.objects.get(pk=5))
        self.assertNotIn(Locations.objects.get(pk=6),iter(areas))

class LoginPageTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


class CreatePageTests(TestCase):
    def test_create_page_status_code(self):
        response = self.client.get('/filter/filters/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('filter:filters'))
        self.assertEquals(response.status_code, 302)

    def test_create_page_status_code_with_auth(self):
        self.user = User.objects.create(username='testuser', password='12345', is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('hello')
        self.user.save()
        user=User.objects.get(username='testuser')
        factory = APIRequestFactory()
        request = factory.get('/filter/filters/')
        force_authenticate(request,user=user)
        request.user=user
        response = views.create(request)
        self.assertEquals(response.status_code, 200)



class UpdatePageTests(TestCase):
    def test_update_page_status_code(self):
        market=Markets(name='Müzik')
        market.save()
        location=Locations(name='Kadıköy')
        location.save()
        user = User.objects.create(username='testuser', password='12345', is_active=True, is_staff=True, is_superuser=True)
        setting=UserMarketSettings(user=user,market=market,location=location)
        response = self.client.get('/filter/edit/1/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_by_name(self):
        market=Markets(name='Müzik')
        market.save()
        location=Locations(name='Kadıköy')
        location.save()
        user = User.objects.create(username='testuser', password='12345', is_active=True, is_staff=True, is_superuser=True)
        setting=UserMarketSettings(user=user,market=market,location=location)
        response = self.client.get(reverse('filter:update', args=('1',)))
        self.assertEquals(response.status_code, 302)

    def test_update_page_status_code_with_auth(self):
        market=Markets(name='Müzik')
        market.save()
        location=Locations(name='Kadıköy')
        location.save()
        self.user = User.objects.create(username='testuser', password='12345', is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('hello')
        self.user.save()
        user=User.objects.get(username='testuser')
        setting=UserMarketSettings(user=user,market=market,location=location)
        factory = APIRequestFactory()
        request = factory.get('/filter/edit/1/')
        force_authenticate(request,user=user)
        request.user=user
        response = views.create(request)
        self.assertEquals(response.status_code, 200)

    def test_update_setting(self):
        market=Markets(name='Müzik')
        market.save()
        location=Locations(name='Kadıköy')
        location.save()
        market2=Markets(name='Ayakkabı')
        market2.save()
        location2=Locations(name='Üsküdar')
        location2.save()
        self.user = User.objects.create(username='testuser', password='12345', is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('hello')
        self.user.save()
        user=User.objects.get(username='testuser')
        setting=UserMarketSettings(user=user,market=market,location=location).save()
        factory = APIRequestFactory()
        request = factory.get('/filter/update/1/')
        force_authenticate(request,user=user)
        request.user=user
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.method='POST'
        request.POST['user']=user
        request.POST['location']=location2.pk
        request.POST['market']=market2.pk
        request.POST._mutable = mutable
        response = views.update(request,pk=1)
        self.assertEqual(UserMarketSettings.objects.count(), 1)
        self.assertEqual(UserMarketSettings.objects.get().market.name, 'Ayakkabı')
