import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Friends, Followers, FriendRequests
from ..serializers import FriendsSerializer, FollowersSerializer, FriendRequestSerializer
from rest_framework.test import APITestCase, URLPatternsTestCase

class FriendRequestAPITest(APITestCase):
    """ Test module for GET all puppies API """
    
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

    def test_get_all_author(self):
        url = "/author/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         


