import pprint
from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Posts
# Create your tests here.
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
# Create your tests here.
User = get_user_model()
class PostsTests(APITestCase):
    urlpatterns = [
        path('api/', include('align.urls')),
    ]
    #url = "/users/register"
    #data = {'username': 'test', 'password': 'securePassword', 'email': 'test@test.com'}
    #user = self.client.post(url, data, format='json')

    def test_Posts(self):
        url = "/users/register"
        data = {'username': 'test', 'password': 'securePassword', 'email': 'test@test.com'}
        user = self.client.post(url, data, format='json')
        self.assertEqual(Posts.objects.count(), 0)
        url = "/posts/"
        user_data = user.data['user']
        data = {'title': 'test_1', 'author': user_data['url']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posts.objects.count(), 1)
        user_data = user.data['user']
        data = {'title': 'test_2', 'author': user_data['url'], 'visibilities': False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posts.objects.count(), 2)
        # get all visible Posts
        url = "/posts/"
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dict = response.data[0]
        self.assertEqual(len(response.data), 1)
        self.assertEqual(dict['id'], 1)
        self.assertEqual(dict['title'], "test_1")
        self.assertEqual(dict['author'], user_data['url'])
        # get posts by specific post_id:
        # test_getPosts_byId :
        url = "/posts/"
        data = {'id': 1}
        response = self.client.get(url, data, format='json')
        dict = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(dict['id'], 1)
        self.assertEqual(dict['title'], "test_1")
        self.assertEqual(dict['author'], user_data['url'])
        # get posts with id (author)
        # test_getPosts_byauthorId(self):
        url = "/posts/user/" + user_data["id"]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        dict = response.data[0]
        self.assertEqual(dict['id'], 2)
        self.assertEqual(dict['title'], "test_2")
        self.assertEqual(dict['author'], user_data['url'])
        dict = response.data[1]
        self.assertEqual(dict['id'], 1)
        self.assertEqual(dict['title'], "test_1")
        self.assertEqual(dict['author'], user_data['url'])
        # get posts which visible to current user
        url = "/posts/"
        data = {'user_id': user_data["id"]}
        response = self.client.get(url, data, format='json')
        dict = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(dict['id'], 1)
        self.assertEqual(dict['title'], "test_1")
        self.assertEqual(dict['author'], user_data['url'])
        # get posts by its author and visible to the current user:
        url = '/posts/author/' + user_data["id"]
        data = {'user_id': user_data["id"]}
        response = self.client.get(url, data, format='json')
        dict = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(dict['id'], 1)
        self.assertEqual(dict['title'], "test_1")
        self.assertEqual(dict['author'], user_data['url'])
        # update a post
        url = '/posts/' + '1/'
        data = {'title': "updated"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], "updated")
        self.assertEqual(response.data['author'], user_data['url'])
        # delete a Post
        url = '/posts/' + '1/'
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Posts.objects.count(), 1)
