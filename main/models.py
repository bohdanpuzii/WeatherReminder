from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications = models.BooleanField(default=True)
    period = models.DurationField(default=timedelta(hours=12))


class Follow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)


def create_task(follow):
    schedule = IntervalSchedule.objects.get_or_create(
        every=follow.profile.period.seconds,
        period=IntervalSchedule.SECONDS
    )
    new_task = PeriodicTask.objects.create(interval=schedule[0], name=follow.id,
                                           task='sender',
                                           args=[follow.id], start_time=timezone.now())
    new_task.save()
    return
