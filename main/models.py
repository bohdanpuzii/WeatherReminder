from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications = models.BooleanField(default=True)


class Follow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    period = models.DurationField(default=timedelta(hours=12))
