from django.contrib.auth.models import User
from django.db import models

import choices


# Create your models here.

class UserData(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=255, choices=choices.GENDER_CHOICES)

    city = models.CharField(max_length=255, null=True, blank=True, default="")
    state = models.CharField(max_length=255, null=True, blank=True, default="")

    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
