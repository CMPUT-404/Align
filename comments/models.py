from django.db import models
from django.utils import timezone
from posts.models import Posts
# Create your models here.
class Comments(models.Model):
    # it has a title
	title = models.CharField(max_length=300)
    # it has a author (many to one)
	root = models.ForeignKey(Posts, on_delete = models.CASCADE)
	plainText = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
