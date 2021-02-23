from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from .forms import LoginByUsernameForm, RegisterForm, SearchForm
from .models import User, Profile, Follow
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from dotenv import load_dotenv
import requests
import os

TOKEN_URL = settings.TOKEN_URL
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')


class FollowCityAPI(APIView):
    def post(self, request, city):
        followed = True
        user_profile = Profile.objects.get(user=request.user)
        if Follow.objects.filter(city=city, profile=user_profile):
            follow_to_delete = Follow.objects.get(city=city, profile=user_profile)
            follow_to_delete.delete()
            followed = False
        else:
            new_follow = Follow(city=city, profile=user_profile)
            new_follow.save()
        return Response({'followed': followed}, status=200)


class NotificationsAPI(APIView):
    def post(self, request):
        user_profile = Profile.objects.get(user=request.user)
        user_profile.notifications = not user_profile.notifications
        user_profile.save()
        return Response({"notifications": user_profile.notifications}, status=200)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            psw = form.cleaned_data['psw']
            new_user = User(username=username, password=psw, email=email)
            new_user.set_password(form.cleaned_data['psw'])
            new_user.save()
            user = authenticate(request, username=username, password=psw)
            new_profile = Profile(user=user)
            new_profile.save()
            response = requests.post(TOKEN_URL,
                                     data={"username": username, "password": psw})
            data = response.json()
            login(request, user)
            header = {'Authorization': 'Bearer ' + data['access']}
            return redirect(reverse('profile'), headers=header)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = LoginByUsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            psw = form.cleaned_data['psw']
            user = authenticate(request, username=username, password=psw)
            if user is not None:
                response = requests.post(TOKEN_URL,
                                         data={"username": username, "password": psw})
                data = response.json()
                login(request, user)
                header = {'Authorization': 'Bearer ' + data['access']}
                return redirect(reverse('profile'), headers=header)
            else:
                return HttpResponse('Incorrect')
    else:
        form = LoginByUsernameForm()
    return render(request, "sign_in.html", {'form': form})


class Search(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = {'city_data': None, 'form': SearchForm}
        return render(request, 'search.html', context=context)

    def post(self, request):
        context = {'city_data': None, 'form': SearchForm}
        form = SearchForm(request.POST)
        if form.is_valid():
            searched_city = form.cleaned_data['search']
            response = requests.get(API_URL, {'city': searched_city, 'key': API_KEY})
            if response.status_code == 200:
                data = response.json()
                context['city_data'] = data['data'][0]
                context['followed'] = True if Follow.objects.filter(profile=Profile.objects.get(user=request.user),
                                                                    city=data['data'][0]['city_name']) else False
            else:
                raise Http404
        return render(request, 'search.html', context=context)


class _Profile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cities_data = []
        for i in Follow.objects.filter(profile=Profile.objects.get(user=request.user)):
            response = requests.get(API_URL, {'city': i.city, 'key': API_KEY})
            data = response.json()
            cities_data.append(data['data'][0])
        context = {'Profile': Profile.objects.get(user=request.user),
                   'Follows': cities_data}
        return render(request, 'profile.html', context=context)


def logout_user(request):
    logout(request)
    return redirect(sign_in)


class SearchAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, city):
        response = requests.get(API_URL, {'city': city, 'key': API_KEY})
        if response.status_code == 200:
            weather = response.json()
            request.session['city'] = weather['data'][0]['city_name']
            return Response(weather)
        else:
            raise Http404

    def post(self, request, city):
        followed = True
        user_profile = Profile.objects.get(user=request.user)
        if Follow.objects.filter(city=request.session['city'], profile=user_profile):
            follow_to_delete = Follow.objects.get(city=request.session['city'], profile=user_profile)
            follow_to_delete.delete()
            followed = False
        else:
            new_follow = Follow(city=request.session['city'], profile=user_profile)
            new_follow.save()
        return Response({'followed': followed}, status=200)
