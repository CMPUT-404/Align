import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Friends, Followers, FriendRequests
from ..serializers import FriendsSerializer, FollowersSerializer, FriendRequestSerializer
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.contrib.auth import get_user_model


User = get_user_model()

class FriendRequestAPITest(APITestCase):
    """ Test module for GET all puppies API """
    
    def setUp(self):
        self.author = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Send", lastName="Request", displayName="send", username="Sending", github="http://github.com")
        self.friend = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Get", lastName="Request", displayName="get", username="Getting", github="http://github.com")
    
    def test_get_all_following(self):
        url = "/following/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_all_friendrequests(self):
        url = "/friendrequest/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_friends(self):
        url = "/friend/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_all_author(self):
        url = "/author/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_friendRequest_bad_data(self):
        self.assertEqual(FriendRequests.objects.count(), 0)
        url = "/friendrequest/"
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendRequests.objects.count(), 0) 

    def test_friendRequest_good_data(self):
        self.assertEqual(FriendRequests.objects.count(), 0)
        url = "/friendrequest/"
        author = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendRequests.objects.count(), 1) 
        
        # test accepting request
        data = {"query": "friendrequestprocess",
                "friendstatus": "accept",
                "author": "http://localhost/author/" + str(self.friend.id) + '/',
                "friend": "http://localhost/author/" + str(self.author.id) + '/'}
        url = "/friend/requestprocess/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendRequests.objects.count(), 0) 

class FriendsFollowsAPITest(APITestCase):

    def setUp(self):
        self.author = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Send", lastName="Request", displayName="send", username="Sending", github="http://github.com")
        self.friend = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Get", lastName="Request", displayName="get", username="Getting", github="http://github.com")
    
        self.assertEqual(Friends.objects.count(), 0)
        self.assertEqual(FriendRequests.objects.count(), 0)
        url = "/friendrequest/"
        author = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendRequests.objects.count(), 1) 
        
        # test accepting request
        data = {"query": "friendrequestprocess",
                "friendstatus": "accept",
                "author": "http://localhost/author/" + str(self.friend.id) + '/',
                "friend": "http://localhost/author/" + str(self.author.id) + '/'}
        url = "/friend/requestprocess/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendRequests.objects.count(), 0)
        self.assertEqual(Friends.objects.count(), 2)
    
    def test_friendsDelete(self):
        
        self.assertEqual(Followers.objects.count(), 0)
        data = {"query": "frienddelete",
                "author": "http://localhost/author/" + str(self.friend.id) + '/',
                "friend": "http://localhost/author/" + str(self.author.id) + '/'}
        url = "/friend/delete/"
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendRequests.objects.count(), 0)
        self.assertEqual(Friends.objects.count(), 0)
        self.assertEqual(Followers.objects.count(), 1)
               
