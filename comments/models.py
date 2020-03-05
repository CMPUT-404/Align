from django.db import models
from django.utils import timezone
from posts.models import Posts
#from django.contrib.auth import get_user_model
# Create your models here.
#User = get_user_model()
# Create your models here.
class Comments(models.Model):
    # it has a title
	id = models.AutoField(primary_key=True)
	# new push test for heroku
	auth = models.TextField()
	#
	root = models.ForeignKey(Posts, related_name='comments', on_delete = models.CASCADE)
	comment = models.TextField()
	publish = models.DateTimeField(blank = True,default=timezone.now)
	test = models.TextField(blank = True,default="test")
