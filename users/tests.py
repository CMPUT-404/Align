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
        response = self.client.get('/author/')
        pprint.pprint(response.data)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    # Test
    # POST /users/register
    # POST /users/login
    # GET /users/
    # GET /users/<id>
    # PATCH /users/<id>
    # GET /users/validate
    def test_user(self):
        self.assertEqual(User.objects.count(), 0)
        url = "/author/register"
        data = {'username': 'test', 'password': 'securePassword', 'email': 'test@test.com'}
        response = self.client.post(url, data, format='json')
        print("###register###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        url = "/author/login"
        data = {'username': 'test', 'password': 'securePassword'}
        response = self.client.post(url, data, format='json')
        print("###login###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        url = "/author/"
        user_url = response.data['user']['url']
        response = self.client.get(url)
        print("###/author/###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 1)

        url = user_url
        response = self.client.get(url)
        print("###GET /author/<id>###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["username"] == "test")
        self.assertTrue(response.data["bio"] == "")

        url = user_url
        data = {'username': 'new_user_name', 'bio': "what's up"}
        response = self.client.patch(url, data, format='json')
        print("###PATCH /author/<id>###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["username"] == 'new_user_name')
        self.assertTrue(response.data["bio"] == "what's up")

        url = "/author/validate"
        response = self.client.get(url)
        print("###GET /author/validate###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['user']["username"] == 'new_user_name')
        self.assertTrue(response.data['user']["bio"] == "what's up")

        url = "/author/search/new_user_name/"
        response = self.client.get(url)
        print("###GET /author/search/<username>###")
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["username"] == 'new_user_name')
        self.assertTrue(response.data["bio"] == "what's up")
        url = "/author/search/notExist/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
