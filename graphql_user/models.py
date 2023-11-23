from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as T

class User(AbstractUser):
    first_name = models.CharField(T("first name"), max_length=150, blank=True)
    last_name = models.CharField(T("last name"), max_length=150, blank=True)
    email = models.EmailField(T("email address"), blank=True)

