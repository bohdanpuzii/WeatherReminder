from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('', views.register, name='register'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('profile', views._Profile.as_view(), name='profile'),
    path('profile/edit', views.edit_period,name='edit_period'),
    path('search', views.Search.as_view(), name='search'),
    path('follow/<str:city>', views.FollowCityAPI.as_view(), name='follow'),
    path('notifications', views.NotificationsAPI.as_view()),
    path('api/weather/<str:city>', views.SearchAPI.as_view()),
    path('logout', views.logout_user, name='logout'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
