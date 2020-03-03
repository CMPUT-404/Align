from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()


class Posts(models.Model):
	# it has a title
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=300)
	# it has a author (many to one)
	author = models.ForeignKey(User, related_name='posts',on_delete = models.CASCADE)
	description = models.TextField(blank=True,max_length=300)
	content = models.TextField(blank=True,max_length=300)
	categories = [
        'web',
        'tutorial'
    ]
	visibilities = models.BooleanField(default = True)
	visible_to = models.TextField(blank=True,max_length=300)

	#images = models.ImageField(blank=True)
	publish = models.DateTimeField(default=timezone.now)
	#author_data = User.objects.prefetch_related('posts')
