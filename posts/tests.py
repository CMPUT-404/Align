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

        url = "/author/register"
        data = {'username': 'test', 'password': 'securePassword', 'email': 'test@test.com'}
        user = self.client.post(url, data, format='json')
        url = "/author/login"
        data = {'username': 'test', 'password': 'securePassword'}
        token = self.client.post(url, data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.data['token'])
        self.access_token = token.data['token']
        # create posts
        url = "/posts/"
        user_data = user.data['user']
        #print("________")
        #print(user_data)
        #print("________")
        data = {'title': 'test_1', 'author_obj': user_data['url']}
        response = self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        header = {'HTTP_ORIGIN': ""}
        response = self.client.post(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posts.objects.count(), 1)
        data = {'title': 'test_2', 'author_obj': user_data['url'], 'visibility': "PRIVATE"}
        response = self.client.post(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posts.objects.count(), 2)
        
        # get all visible Posts
        url = "/posts"
        #response = self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dict = response.data['posts'][0]
        self.assertEqual(dict['id'], 1)
        self.assertEqual(dict['title'], "test_1")
        # get posts by specific post_id:
        # test_getPosts_byId :
        url = "/posts/1/"
        response = self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        response = self.client.get(url)
        dict = response.data['post']
        #print(dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict['id'], 1)
        self.assertEqual(dict['title'], "test_1")

        url = "/posts/2/"
        response = self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        response = self.client.get(url)
        dict = response.data['post']
        #print(dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict['id'], 2)
        self.assertEqual(dict['title'], "test_2")
        # get posts with id (author)
        # test_getPosts_byauthorId(self):
        url = "/posts/author/"+ user_data["id"][-37:-1]
        response = self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dict = response.data['posts']
        self.assertEqual(dict[0]['id'], 2)
        self.assertEqual(dict[0]['title'], "test_2")
        self.assertEqual(dict[0]['author_obj'], user_data['url'])
        self.assertEqual(dict[1]['id'], 1)
        self.assertEqual(dict[1]['title'], "test_1")
        self.assertEqual(dict[1]['author_obj'], user_data['url'])
    
        # get posts which visible to current user
        url = "/author/posts"
        response = self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dict = response.data['posts']
        self.assertEqual(dict[0]['id'], 2)
        self.assertEqual(dict[0]['title'], "test_2")
        self.assertEqual(dict[0]['author_obj'], user_data['url'])
        self.assertEqual(dict[1]['id'], 1)
        self.assertEqual(dict[1]['title'], "test_1")
        self.assertEqual(dict[1]['author_obj'], user_data['url'])
        
        # get posts by its author and visible to the current user:
        url = '/author/' + user_data["id"][-37:-1] + '/posts'
        response = self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dict = response.data['posts']
        self.assertEqual(dict[0]['id'], 2)
        self.assertEqual(dict[0]['title'], "test_2")
        self.assertEqual(dict[0]['author_obj'], user_data['url'])
        self.assertEqual(dict[1]['id'], 1)
        self.assertEqual(dict[1]['title'], "test_1")
        self.assertEqual(dict[1]['author_obj'], user_data['url'])

        # update a post
        url = '/posts/' + '1/'
        data = {'title': "updated"}
        response = self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], "updated")
        self.assertEqual(response.data['author_obj'], user_data['url'])
        # delete a Post
        url = '/posts/' + '1/'
        response = self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Posts.objects.count(), 1)