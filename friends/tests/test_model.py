from django.test import TestCase
from ..models import Friends
from django.contrib.auth import get_user_model


User = get_user_model()


class FriendTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):        
        self.author = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Send", lastName="Request", displayName="send1", github="http://github.com")
        self.friend = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Get", lastName="Request", displayName="get1", github="http://github.com")
        
        Friends.objects.create(author=self.author, friend=self.friend)
        Friends.objects.create(author=self.friend, friend=self.author)

    def test_friend(self):
        friend1 = Friends.objects.get(author=self.author.id)
        friend2 = Friends.objects.get(friend=self.friend.id)
        self.assertEqual(friend1.author.firstName, "Send")
        self.assertEqual(friend2.author.firstName, "Get")
