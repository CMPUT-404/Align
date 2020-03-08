from django.test import TestCase
from ..models import Friends, Followers, FriendRequests
from django.contrib.auth import get_user_model


User = get_user_model()


class FriendsTest(TestCase):
    """ Test module for Friends model """

    def setUp(self):        
        self.author = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Send", lastName="Request", displayName="send", username="Sending", github="http://github.com")
        self.friend = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Get", lastName="Request", displayName="get", username="Getting", github="http://github.com")
        
        Friends.objects.create(author=self.author, friend=self.friend)
        Friends.objects.create(author=self.friend, friend=self.author)

    def test_FriendAuthor(self):
        friend1 = Friends.objects.get(author=self.author.id)
        friend2 = Friends.objects.get(author=self.friend.id)
        self.assertEqual(friend1.author.firstName, "Send")
        self.assertEqual(friend2.author.firstName, "Get")
        
    def test_FriendFriend(self):
        friend1 = Friends.objects.get(author=self.author.id)
        friend2 = Friends.objects.get(author=self.friend.id)
        self.assertEqual(friend1.friend.firstName, "Get")
        self.assertEqual(friend2.friend.firstName, "Send")
        
        
        
class FriendRequestsTest(TestCase):
    """ Test module for FriendRequests model """

    def setUp(self):        
        self.author = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Send", lastName="Request", displayName="send", username="Sending", github="http://github.com")
        self.friend = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Get", lastName="Request", displayName="get", username="Getting", github="http://github.com")
        
        FriendRequests.objects.create(authorID=self.author, friendID=self.friend)

    def test_FriendRequestAuthor(self):
        friend1 = FriendRequests.objects.get(authorID=self.author.id)
        self.assertEqual(friend1.authorID.firstName, "Send")
        
    def test_FriendRequestFriend(self):
        friend1 = FriendRequests.objects.get(authorID=self.author.id)
        self.assertEqual(friend1.friendID.firstName, "Get")



class FollowersTest(TestCase):
    """ Test module for Followers model """

    def setUp(self):        
        self.author = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Send", lastName="Request", displayName="send", username="Sending", github="http://github.com")
        self.friend = User.objects.create(bio="bio", host="http://localhost:8000", firstName="Get", lastName="Request", displayName="get", username="Getting", github="http://github.com")
        
        Followers.objects.create(author=self.author, following=self.friend)

    def test_FollowersAuthor(self):
        friend1 = Followers.objects.get(author=self.author.id)
        self.assertEqual(friend1.author.firstName, "Send")
        
    def test_FollowersFollowing(self):
        friend1 = Followers.objects.get(author=self.author.id)
        self.assertEqual(friend1.following.firstName, "Get")      