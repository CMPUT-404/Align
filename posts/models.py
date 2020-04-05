from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
import uuid
# Create your models here.
User = get_user_model()


class Posts(models.Model):
	# it has a title
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=300)
	# it has a author (many to one)
	author_obj = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
	description = models.TextField(blank=True, max_length=300)
	content = models.TextField(blank=True, max_length=300)
	contentType = models.TextField(blank=True, max_length=300)
	visibility = models.TextField(blank=True, default="PUBLIC", max_length=300)
	visibleTo = models.TextField(blank=True, max_length=300)
	image = models.TextField(blank=True)
	published = models.DateTimeField(blank=True,default=timezone.now)
	source = models.URLField(blank=True)
	origin = models.URLField(blank=True)
	unlisted = models.BooleanField(default=False)



class Server(models.Model):
	id = models.AutoField(primary_key=True)
	domain = models.URLField(max_length=300, unique=True)
	status = models.BooleanField(default=True)
