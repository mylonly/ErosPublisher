from django.test import TestCase
from rest_framework.test import APIRequestFactory,APIClient,APITestCase, URLPatternsTestCase
from .views import *
from .models import UserProfile
import json
from django.urls import include, path, reverse

# Create your tests here.


class AuthTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('auth/', include('Auth.urls')),
    ]
    def setUp(self):
        UserProfile.objects.create_superuser(username="txg", password="1234tv.com", avatar="http://www.baidu.com", role="admin", email="txg@1234tv.com")


    def test_login(self):
        url = reverse(login().get_view_name())
        data = {"username":"txg", "password":"1234tv.com"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(json.loads(response.content), {"resCode": 0, "msg": "操作成功", "detail": None, "data": None})


