from django.db import models
from django.utils import timezone
from posts.models import Posts
import uuid
#from django.contrib.auth import get_user_model
# Create your models here.
#User = get_user_model()
# Create your models here.
class Comments(models.Model):
    # it has a title
	id = models.AutoField(primary_key=True)
	#id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	# new push test for heroku
	#auth = models.TextField()
	auth_id = models.TextField(blank=True, max_length=300)
	url = models.TextField(blank=True, max_length=300)
	host = models.TextField(blank=True, max_length=300)
	name = models.TextField(blank=True, max_length=300)
	github = models.TextField(blank=True, max_length=300)
	content = models.TextField(blank=True, max_length=300)
	#
	root = models.ForeignKey(Posts, related_name='comments', on_delete = models.CASCADE)
	comment = models.TextField(blank=True, max_length=300)
	#comment = models.TextField()
	published = models.DateTimeField(blank = True,default=timezone.now)
	#est = models.TextField(blank = True,default="test")
