from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from users.apps import UsersConfig
from users.views import UserListView, UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    # path('login/', UserLogin.as_view(), name='login'),
    # path('logout/', UserLogout.as_view(), name='logout'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('list/', UserListView.as_view(), name='list'),
    path('create/', UserCreateView.as_view(), name='create'),

    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),

    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'),
]
