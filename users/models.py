import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO: AUTOCOMPLETE FOR HOST AND DISPLAY NAME
# TODO: FRIENDS


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(max_length=500, null=True, blank=True)
    host = models.URLField(blank=True, null=True, default="127.0.0.1:8000")  # FIXME HARDCODED HOST
    firstName = models.CharField(max_length=20, null=True, blank=True)
    lastName = models.CharField(max_length=20, null=True, blank=True)
    displayName = models.CharField(max_length=40, null=True, blank=True, default="{} {}".format(str(firstName), str(lastName)))
    github = models.URLField(blank=True, null=True,)

