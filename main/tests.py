from django.test import TestCase, Client
from .models import Profile, Follow, User
from django.urls import reverse


class ModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TEST')
        self.profile = Profile.objects.create(user=self.user)
        self.follow = Follow.objects.create(profile=self.profile, city='Kyiv')

    def test_model(self):
        self.assertTrue(self.profile.notifications)
        self.assertEqual(self.user.username, 'TEST')
        self.assertEqual(self.follow.city, 'Kyiv')


class ViewTest(TestCase):
    def test_views(self):
        client = Client()
        response = client.get(reverse('sign_in'))
        self.assertEqual(response.status_code, 200)
        response = client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        response = client.post(
            reverse('register'), {'email': 'test@gmail.com', 'username': 'test', 'psw': 'test123123'})
        self.assertRedirects(response, reverse('profile'), status_code=302)
        response = client.get(reverse('logout'))
        self.assertRedirects(response, reverse('sign_in'), status_code=302)
        response = client.post(reverse('sign_in'), {'username': 'test', 'psw': 'test123123'})
        self.assertRedirects(response, reverse('profile'), status_code=302)
        response = client.post(reverse('search'), {'search': 'Toronto'})
        self.assertEqual(response.status_code, 200)
        response = client.post(reverse('follow', args={'city': 'Toronto'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Follow.objects.filter(profile=Profile.objects.get(user=User.objects.get(username='test'))).exists())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Follow.objects.filter(profile=Profile.objects.get(user=User.objects.get(username='test')), city='Kyiv').exists())
