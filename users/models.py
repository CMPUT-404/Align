import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO: AUTOCOMPLETE FOR HOST AND DISPLAY NAME
# TODO: FRIENDS


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(max_length=500, null=True, blank=True)
    host = models.URLField(blank=True, null=True)
    firstName = models.CharField(max_length=20, null=True, blank=True)
    lastName = models.CharField(max_length=20, null=True, blank=True)
    displayName = models.CharField(max_length=40, null=True, blank=True)
    github = models.CharField(max_length=40, blank=True, null=True,)

    def save(self, *args, **kwargs):
        self.generate_display_name()
        super(User, self).save(*args, **kwargs)

    def generate_display_name(self):
        if not self.displayName:
            if self.firstName and self.lastName:
                self.displayName = "{} {}".format(self.firstName, self.lastName)
            elif self.firstName:
                self.displayName = self.firstName
            elif self.lastName:
                self.displayName = self.lastName
            else:
                self.displayName = self.username

