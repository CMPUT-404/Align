from django.test import TestCase
from ..models import Following

class FriendsTest(TestCase):
    """ Test module for Friends model """

    def setUp(self):        
        self.senderUrl = "http://localhost:8000/author/1234"
        self.receiverUrl = "http://localhost:8000/author/5678"
        Following.objects.create(sender=self.senderUrl, receiver=self.receiverUrl, status=None)

    def test_FriendAuthor(self):
        friend = Following.objects.get(sender=self.senderUrl)
        self.assertEqual(friend.sender, self.senderUrl)
        self.assertNotEqual(friend.receiver, self.senderUrl)
        self.assertEqual(friend.receiver, self.receiverUrl)
        self.assertNotEqual(friend.sender, self.receiverUrl)
        self.assertEqual(friend.status, None)