from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Enter your email:')
    username = forms.CharField(label='Enter your username')
    psw = forms.CharField(widget=forms.PasswordInput, label='Your password')


class LoginByUsernameForm(forms.Form):
    username = forms.CharField(label='Enter your username')
    psw = forms.CharField(widget=forms.PasswordInput, label='Your password')


class SearchForm(forms.Form):
    search = forms.CharField(label='Enter city name', required=False)
