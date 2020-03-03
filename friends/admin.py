from django.contrib import admin
from friends.models import FriendRequests
from friends.models import Followers
from friends.models import Friends

admin.site.register(FriendRequests)
admin.site.register(Followers)
admin.site.register(Friends)
# Register your models here.
