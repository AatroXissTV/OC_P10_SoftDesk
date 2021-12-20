# django imports
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

# django rest framework imports


class User(AbstractBaseUser):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=108)
    last_name = models.CharField(max_length=108)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=108)
