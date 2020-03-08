import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Friends, Followers, FriendRequests
from ..serializers import FriendsSerializer, FollowersSerializer, FriendRequestSerializer

# initialize the APIClient app
client = Client()


