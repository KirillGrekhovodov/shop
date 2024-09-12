from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True, )
    subscriber = models.ManyToManyField('self', related_name="followers")
