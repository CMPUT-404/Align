import pprint

from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

User = get_user_model()

class AccountTests(APITestCase):
    urlpatterns = [
        path('api/', include('align.urls')),
    ]

    # Test /users without authorization, should return an error
    def test_unauthorized_users(self):
        """
        get /users without authenticated
        """
        response = self.client.get('/users/')
        pprint.pprint(response.data)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    # Test
    # POST /users/register
    # POST /users/login
    # GET /user/
    # GET /user/<id>
    # PATCH /user/<id>
    def test_user(self):
        self.assertEqual(User.objects.count(), 0)
        url = "/users/register"
        data = {'username': 'test', 'password': 'securePassword', 'email': 'test@test.com'}
        response = self.client.post(url, data, format='json')
        print("###register###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        url = "/users/login"
        data = {'username': 'test', 'password': 'securePassword'}
        response = self.client.post(url, data, format='json')
        print("###login###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        url = "/users/"
        user_url = response.data['user']['url']
        response = self.client.get(url)
        print("###/users/###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 1)

        url = user_url
        response = self.client.get(url)
        print("###GET /users/<id>###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["host"] == "127.0.0.1")
        self.assertTrue(response.data["username"] == "test")
        self.assertTrue(response.data["bio"] == "")

        url = user_url
        data = {'username': 'new_user_name', 'bio': "what's up"}
        response = self.client.patch(url, data, format='json')
        print("###PATCH /users/<id>###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["host"] == "127.0.0.1")
        self.assertTrue(response.data["username"] == 'new_user_name')
        self.assertTrue(response.data["bio"] == "what's up")

