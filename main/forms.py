from django import forms
from datetime import timedelta

PERIOD_CHOICES = (
    (timedelta(minutes=1), '1 min'),
    (timedelta(hours=1), '1 hour'),
    (timedelta(hours=6), '6 hour'),
    (timedelta(hours=12), '12 hour')
)
NOTIFICATION_CHOICES = ((True, "Enable"), (False, 'Disable'))


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Enter your email:')
    username = forms.CharField(label='Enter your username')
    psw = forms.CharField(widget=forms.PasswordInput, label='Your password')


class LoginByUsernameForm(forms.Form):
    username = forms.CharField(label='Enter your username')
    psw = forms.CharField(widget=forms.PasswordInput, label='Your password')


class SearchForm(forms.Form):
    search = forms.CharField(label='Enter city name', required=False)


class ChangePeriodForm(forms.Form):
    period = forms.ChoiceField(choices=PERIOD_CHOICES, label='Choose period of notifications')
    notifications = forms.ChoiceField(choices=NOTIFICATION_CHOICES, label='Enable or disable notifications')
