from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
# Create your models here.
User = get_user_model()


class Posts(models.Model):
	# it has a title
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=300)
	# it has a author (many to one)
	author_obj = models.ForeignKey(User, related_name='posts',on_delete = models.CASCADE)
	description = models.TextField(blank=True,max_length=300)
	content = models.TextField(blank=True,max_length=300)
	categories = [
        'web',
        'tutorial'
    ]
	#visibility = models.BooleanField(default = True)
	visibility = models.TextField(blank=True,default = "PUBLIC",max_length=300)
	visibleTo = models.TextField(blank=True)
	image = models.TextField(blank=True,max_length=300)
	published = models.DateTimeField(blank=True,default=timezone.now)
	#author_data = User.objects.prefetch_related('posts')


class Server(models.Model):
	id = models.AutoField(primary_key=True)
	domain = models.URLField(max_length=300, unique=True)
	status = models.BooleanField(default=True)
