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

    def test_create_setting(self):
        """
        Ensure we can create a new account object.
        """
        market=Markets(name='Müzik')
        market.save()
        location=Locations(name='Kadıköy')
        location.save()
        self.user = User.objects.create(username='testuser', password='12345', is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('hello')
        self.user.save()
        user=User.objects.get(username='testuser')
        factory = APIRequestFactory()
        request = factory.get('/filter/filters/')
        force_authenticate(request,user=user)
        request.user=user
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.method='POST'
        request.POST['user']=user
        request.POST['location']=location.pk
        request.POST['market']=market.pk
        request.POST._mutable = mutable
        response = views.create(request)
        self.assertEqual(UserMarketSettings.objects.count(), 1)
        self.assertEqual(UserMarketSettings.objects.get().market.name, 'Müzik')

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
        """
        Ensure we can create a new account object.
        """
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
        setting=UserMarketSettings(user=user,market=market,location=location)
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
        response = views.create(request)
        self.assertEqual(UserMarketSettings.objects.count(), 1)
        self.assertEqual(UserMarketSettings.objects.get().market.name, 'Ayakkabı')
