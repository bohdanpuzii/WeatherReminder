import os
from django.core.mail import send_mail
import requests

from .models import Follow
from WeatherReminder.celery import app

API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')


@app.task(name='sender')
def sender(sub_id):
    follow = Follow.objects.get(id=sub_id)
    response = requests.get(API_URL, {'city': follow.city, 'key': API_KEY})
    send_mail('Weather forecast', response.text,
              'bogdan.puziy@gmail.com', [follow.profile.user.email], fail_silently=False)
    return
