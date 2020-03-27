from rest_framework import status
from ..models import Following
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


User = get_user_model()

class FriendsAPITest(APITestCase):
    """ Test module for GET all puppies API """
    
    def setUp(self):
    
        url = "/author/register"
        data = {'username': 'Testing', 'password': 'password', 'email': 'test@gmail.com'}
        response = self.client.post(url, data, format='json')

        url = "/author/login"
        data = {'username': 'Testing', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    
        self.author = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Send", lastName="Request", displayName="send", username="Sending", github="http://github.com")
        self.friend = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Get", lastName="Request", displayName="get", username="Getting", github="http://github.com")
    
    def test_get_all_friendrequests(self):
        url = "/friendrequest/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_friendRequest_bad_data(self):
        self.assertEqual(Following.objects.count(), 0)
        data = {}
        url = "/friendrequest/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Following.objects.count(), 0) 

    def test_friendRequest_process(self):
        
        
        # send friend request
        self.assertEqual(Following.objects.count(), 0)
        author = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Following.objects.count(), 1) 
                
        
        # send duplicate friend request
        self.assertEqual(Following.objects.count(), 1)
        author = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Following.objects.count(), 1) 
        
        
        # send reverse request
        self.assertEqual(Following.objects.count(), 1)
        author = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        friend = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(Following.objects.count(), 2)
        
        
        # test bad reject
        author = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id) + "1234",
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/reject/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
        
        # test good reject
        author = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/reject/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        # test Bad accepting request
        author = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/accept/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        # test good accepting request
        author = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        friend = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/accept/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        # test Bad delete friend request
        author = {"id": "http://localhost/author/" + str(self.author.id) + "123",
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/deletefriend/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
        # test good delete friend request
        author = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/deletefriend/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        
        
        # test bad delete following
        author = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        friend = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/deletefollowing/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
        
        # test good delete following
        author = {"id": "http://localhost/author/" + str(self.friend.id),
                  "host": self.friend.host,
                  "displayName": self.friend.displayName,
                  "url": "http://localhost/author/" + str(self.friend.id)}
        friend = {"id": "http://localhost/author/" + str(self.author.id),
                  "host": self.author.host,
                  "displayName": self.author.displayName,
                  "url": "http://localhost/author/" + str(self.author.id)}
        data = {"query": "friendrequest", "author": author, "friend": friend}
        url = "/friendrequest/deletefollowing/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK) 