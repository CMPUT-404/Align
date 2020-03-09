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

    def test_createPosts(self):
        url = "/users/register"
        data = {'username': 'test', 'password': 'securePassword', 'email': 'test@test.com'}
        user = self.client.post(url, data, format='json')
        self.assertEqual(Posts.objects.count(), 0)
        url = "/posts"
        print(user.data["url"])
        data = {'title': 'test', 'author': user.data["url"]}
        response = self.client.post(url, data, format='json')
        pprint.pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posts.objects.count(), 1)
    # get posts without id
    def test_getPosts(self):
        pass

    # get posts with id (to current user)
    def test_getPosts_byUserId(self):
        pass

    # get posts by specific post_id:
    def test_getPosts_byPostId(self):
        pass

    # get posts by its author and visible to the current user:
    def test_postsAuthorUser(self):
        pass
    # update a post
    def test_updatePost(self):
        pass

    # delete a Post
    def test_delete_Post(self):
        pass

    # get posts made by one user
    def test_getPost_madeBy(self):
        pass
