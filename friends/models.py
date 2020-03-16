import uuid

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


#class User(AbstractUser):
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    bio = models.TextField(max_length=500, blank=True)
#    host = models.URLField(blank=True, default="127.0.0.1:8000")  # FIXME HARDCODED HOST
#    firstName = models.CharField(max_length=20, blank=True)
#    lastName = models.CharField(max_length=20, blank=True)
#    displayName = models.CharField(max_length=40, blank=True, default="{} {}".format(firstName, lastName))
#    github = models.URLField(blank=True)

class FriendRequests(models.Model):
    authorID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authorID')
    friendID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendID')
    
class Followers(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Follower_author')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
class Friends(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Friends_author')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')


# new following
class Following(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    # Status: {
    # True: both are friend, can be rejected (back to single-directionally without request notification)
    # False: sender follows receiver single-directionally,
    # None: A friend request has sent, can be rejected or accepted, sender follows receiver single-directionally,
    # }
    status = models.BooleanField(null=True, default=None)

    class Meta:
        unique_together = ["sender", "receiver"]  # this prevent duplicate
